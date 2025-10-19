#!/usr/bin/env python3
"""
Integrated Advanced Test Generation Engine
Combines basic and advanced analysis for comprehensive test generation
"""

import os
import sys
import tempfile
import subprocess
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
import networkx as nx
import re
from dotenv import load_dotenv
import time
from datetime import datetime

# === Load .env configuration ===
load_dotenv()

# Environment variables
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "codellama:instruct")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10000"))
LOCAL_SERVER_URL = os.getenv("LOCAL_SERVER_URL", "http://localhost:3000")
MAX_WAIT_SECONDS = int(os.getenv("MAX_WAIT_SECONDS", "30"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Dynamic paths - will be set per run
LOG_DIR = None
TEST_OUTPUT_DIR = None
REPORT_DIR = None
RUN_DIR = None

class IntegratedTestGenerator:
    """Integrated test generator combining basic and advanced analysis"""
    
    def __init__(self, run_timestamp=None):
        self.temp_dir = None
        self.framework = None
        self.files = []
        self.file_roles = {}
        self.route_map = {}
        self.run_timestamp = run_timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.activity_log_file = None
        
        # Only create directories if this is a real run (not just importing)
        if run_timestamp is not None or self._is_main_execution():
            self._setup_run_directories()
            self._init_activity_log()
            print("🚀 Integrated Advanced Test Generation Engine")
            print("=" * 60)
    
    def _is_main_execution(self):
        """Check if this is being run as the main script (not imported)"""
        import sys
        return hasattr(sys, 'ps1') or sys.argv[0].endswith('integrated_test_generator.py')
    
    def _setup_run_directories(self):
        """Setup timestamped folder structure for this run"""
        global LOG_DIR, TEST_OUTPUT_DIR, REPORT_DIR, RUN_DIR
        
        # Create main run_files directory and run directory
        RUN_DIR = os.path.join("run_files", f"run_{self.run_timestamp}")
        os.makedirs(RUN_DIR, exist_ok=True)
        
        # Create subdirectories
        LOG_DIR = os.path.join(RUN_DIR, "logs")
        TEST_OUTPUT_DIR = os.path.join(RUN_DIR, "tests")
        REPORT_DIR = os.path.join(RUN_DIR, "reports")
        
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        os.makedirs(REPORT_DIR, exist_ok=True)
        
        print(f"📁 Created run directory: {RUN_DIR}")
        print(f"📁 Logs: {LOG_DIR}")
        print(f"📁 Tests: {TEST_OUTPUT_DIR}")
        print(f"📁 Reports: {REPORT_DIR}")
    
    def _init_activity_log(self):
        """Initialize comprehensive activity logging"""
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            self.activity_log_file = f"{LOG_DIR}/activity_log_{self.run_timestamp}.txt"
            with open(self.activity_log_file, 'w', encoding='utf-8') as f:
                f.write(f"AI Playwright Test Generator - Activity Log\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
            print(f"📝 Activity log initialized: {self.activity_log_file}")
        except Exception as e:
            print(f"❌ Error initializing activity log: {e}")
            self.activity_log_file = None
    
    def _log_activity(self, message: str, level: str = "INFO"):
        """Log activity to comprehensive log file"""
        if self.activity_log_file:
            try:
                timestamp = datetime.now().strftime('%H:%M:%S')
                with open(self.activity_log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] [{level}] {message}\n")
            except Exception as e:
                print(f"❌ Error writing to activity log: {e}")
    
    def _parse_user_flows(self, user_flows_content: str) -> List[Dict[str, str]]:
        """Parse user flows content to extract individual flows"""
        flows = []
        lines = user_flows_content.split('\n')
        current_flow = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('## Flow:'):
                # Save previous flow if exists
                if current_flow:
                    flows.append(current_flow)
                
                # Start new flow
                flow_name = line.replace('## Flow:', '').strip()
                current_flow = {
                    'name': flow_name,
                    'content': line + '\n',
                    'filename': self._generate_flow_filename(flow_name)
                }
            elif current_flow:
                current_flow['content'] += line + '\n'
        
        # Add the last flow
        if current_flow:
            flows.append(current_flow)
        
        self._log_activity(f"Parsed {len(flows)} user flows from content")
        return flows
    
    def _generate_flow_filename(self, flow_name: str) -> str:
        """Generate filename for a user flow"""
        # Convert flow name to filename
        filename = flow_name.lower()
        filename = filename.replace(' ', '_')
        filename = filename.replace(':', '')
        filename = filename.replace('-', '_')
        filename = filename.replace('__', '_')
        return f"{filename}.spec.ts"
    
    def _generate_test_for_flow(self, flow: Dict[str, str], app_analysis: Dict[str, Any]) -> str:
        """Generate comprehensive test for a specific user flow"""
        flow_name = flow['name']
        flow_content = flow['content']
        filename = flow['filename']
        
        print(f"🔄 Generating comprehensive test for: {flow_name}")
        self._log_activity(f"Generating test for flow: {flow_name}")
        
        # Build focused prompt for this specific flow
        prompt = f"""You are a senior QA automation architect specializing in Playwright test generation.

Your task is to generate a COMPREHENSIVE Playwright test file for the following specific user flow.

**CRITICAL REQUIREMENTS:**
1. Generate ONLY the test file for this specific user flow
2. Create ALL necessary test cases to cover this flow completely
3. Include success paths, error paths, validation scenarios, and edge cases
4. Use the exact routes, components, UI elements, and API endpoints from the flow
5. NO OUTPUT LIMITS - generate as many test cases as needed for complete coverage
6. Make the tests realistic and actionable

**USER FLOW TO TEST:**
{flow_content}

**APPLICATION CONTEXT:**
Framework: {self.framework}
Routes: {list(self.route_map.keys())[:10]}
Components: {list(self.file_roles.keys())[:20]}

**REQUIRED OUTPUT FORMAT:**
{filename}:
```typescript
import {{ test, expect }} from '@playwright/test';

// Comprehensive test suite for {flow_name}
test.describe('{flow_name}', () => {{
  // Generate ALL test cases needed for complete coverage
  // Include success paths, error paths, validation, edge cases
  // Use exact routes, components, and API endpoints from the flow
}});
```

**IMPORTANT:**
- Generate COMPLETE test coverage for this user flow
- Include proper imports, test structure, and assertions
- Use realistic test data and API mocking
- Test all steps and scenarios described in the flow
- Make sure the code is syntactically correct and complete
- NO LIMITS on number of test cases - create comprehensive coverage"""

        # Save individual flow prompt to logs
        flow_prompt_file = f"{LOG_DIR}/flow_prompt_{self.run_timestamp}_{filename.replace('.spec.ts', '')}.txt"
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(flow_prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"📝 Flow prompt saved to: {flow_prompt_file}")
        self._log_activity(f"Flow prompt saved: {flow_prompt_file}")
        
        # Call Ollama with NO output limits
        request_data = {
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False,
            'options': {
                'num_predict': -1,  # NO LIMITS - let LLM generate all needed tests
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40
            }
        }
        
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json=request_data,
                timeout=300  # Increased timeout for comprehensive generation
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                print(f"✅ Generated comprehensive test for {flow_name}: {len(response_text)} characters")
                self._log_activity(f"Generated comprehensive test for {flow_name}: {len(response_text)} characters")
                
                # Save response to logs
                response_file = f"{LOG_DIR}/flow_response_{self.run_timestamp}_{filename.replace('.spec.ts', '')}.txt"
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(response_text)
                print(f"📝 Flow response saved to: {response_file}")
                self._log_activity(f"Flow response saved: {response_file}")
                
                # Parse the response to extract just the test content
                test_content = self._extract_test_content_from_response(response_text, filename)
                return test_content
            else:
                error_msg = f"Ollama request failed for {flow_name}: {response.status_code}"
                print(f"❌ {error_msg}")
                self._log_activity(error_msg, "ERROR")
                return ""
        except Exception as e:
            error_msg = f"Error calling Ollama for {flow_name}: {e}"
            print(f"❌ {error_msg}")
            self._log_activity(error_msg, "ERROR")
            return ""
    
    def _extract_test_content_from_response(self, response_text: str, filename: str) -> str:
        """Extract test content from LLM response"""
        lines = response_text.split('\n')
        in_code_block = False
        test_content = []
        
        for line in lines:
            if line.strip().startswith(f"{filename}:"):
                continue
            elif line.strip().startswith('```typescript'):
                in_code_block = True
                continue
            elif line.strip() == '```' and in_code_block:
                break
            elif in_code_block:
                test_content.append(line)
        
        return '\n'.join(test_content)
    
    def generate_tests(self, repo_url: str, output_dir: str = "tests") -> Dict[str, Any]:
        """Main test generation pipeline"""
        try:
            self._log_activity(f"Starting test generation for: {repo_url}")
            
            # Step 1: Process repository (clone or use local)
            print("\n📥 STEP 1: PROCESSING REPOSITORY")
            print("-" * 40)
            self._log_activity("STEP 1: PROCESSING REPOSITORY", "STEP")
            self.temp_dir = self._clone_repository(repo_url)
            self._log_activity(f"Repository processed: {self.temp_dir}")
            
            # Step 2: Detect framework
            print("\n🔍 STEP 2: DETECTING FRAMEWORK")
            print("-" * 40)
            self._log_activity("STEP 2: DETECTING FRAMEWORK", "STEP")
            self.framework = self._detect_framework()
            self._log_activity(f"Framework detected: {self.framework}")
            
            # Step 3: Collect source files
            print("\n📁 STEP 3: COLLECTING SOURCE FILES")
            print("-" * 40)
            self._log_activity("STEP 3: COLLECTING SOURCE FILES", "STEP")
            self.files = self._collect_source_files()
            self._log_activity(f"Source files collected: {len(self.files)} files")
            
            # Step 4: Build dependency graph
            print("\n🕸️ STEP 4: BUILDING DEPENDENCY GRAPH")
            print("-" * 40)
            self._log_activity("STEP 4: BUILDING DEPENDENCY GRAPH", "STEP")
            graph, file_roles, route_map = self._build_dependency_graph(self.files)
            self.file_roles = file_roles
            self.route_map = route_map
            self._log_activity(f"Dependency graph built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
            
            # Step 5: Export Graphviz
            print("\n📊 STEP 5: EXPORTING GRAPHVIZ")
            print("-" * 40)
            self._log_activity("STEP 5: EXPORTING GRAPHVIZ", "STEP")
            self._export_graphviz(graph, file_roles)
            
            # Step 5.5: Perform comprehensive application analysis
            print("\n🔍 STEP 5.5: COMPREHENSIVE APPLICATION ANALYSIS")
            print("-" * 40)
            app_analysis = self._analyze_application_functionality()
            
            # Step 5.6: Generate User Flow Description Report
            print("\n📋 STEP 5.6: GENERATING USER FLOW DESCRIPTION REPORT")
            print("-" * 40)
            self._log_activity("STEP 5.6: GENERATING USER FLOW DESCRIPTION REPORT", "STEP")
            user_flows_content = self._generate_user_flows_report(app_analysis)
            self._log_activity(f"User flows report generated: {len(user_flows_content)} characters")
            
            # Step 6: Parse user flows and generate tests per flow
            print("\n🤖 STEP 6: GENERATING TESTS PER USER FLOW")
            print("-" * 40)
            self._log_activity("STEP 6: GENERATING TESTS PER USER FLOW", "STEP")
            
            # Parse user flows
            user_flows = self._parse_user_flows(user_flows_content)
            self._log_activity(f"Found {len(user_flows)} user flows to generate tests for")
            
            # Generate one test spec per user flow
            test_files = []
            for i, flow in enumerate(user_flows, 1):
                print(f"\n📝 Generating test for flow {i}/{len(user_flows)}: {flow['name']}")
                self._log_activity(f"Generating test for flow: {flow['name']}")
                
                # Generate test for this specific flow
                test_content = self._generate_test_for_flow(flow, app_analysis)
                if test_content:
                    # Save the test file
                    success = self._save_file(flow['filename'], test_content)
                    if success:
                        test_files.append(flow['filename'])
                        self._log_activity(f"Successfully generated test file: {flow['filename']}")
                    else:
                        self._log_activity(f"Failed to save test file: {flow['filename']}", "ERROR")
                else:
                    self._log_activity(f"Failed to generate test content for: {flow['name']}", "ERROR")
            
            self._log_activity(f"Generated {len(test_files)} test files from {len(user_flows)} user flows")
            
            # Step 7: Validate tests
            print("\n✅ STEP 7: VALIDATING TESTS")
            print("-" * 40)
            self._log_activity("STEP 7: VALIDATING TESTS", "STEP")
            validation_results = self._validate_tests(test_files)
            self._log_activity(f"Test validation completed: {validation_results}")
            
            # Step 8: Generate comprehensive report
            print("\n📊 STEP 8: GENERATING COMPREHENSIVE REPORT")
            print("-" * 40)
            self._log_activity("STEP 8: GENERATING COMPREHENSIVE REPORT", "STEP")
            report = self._generate_comprehensive_report(app_analysis, validation_results)
            self._save_report(report)
            self._log_activity(f"Comprehensive report generated and saved: {len(report)} characters")
            
            print("\n🎉 Test generation completed successfully!")
            print(f"Framework: {self.framework}")
            print(f"Files analyzed: {len(self.files)}")
            print(f"Dependency graph nodes: {len(graph.nodes())}")
            print(f"Generated {len(test_files)} test files")
            print(f"Analysis report: {os.path.join(RUN_DIR, 'reports', 'analysis_report.md')}")
            print(f"Graphviz file: {os.path.join(RUN_DIR, 'code_graph.dot')}")
            print(f"Run directory: {RUN_DIR}")
            
            self._log_activity("Test generation completed successfully", "SUCCESS")
            self._log_activity(f"Final results: {len(test_files)} test files, {len(self.files)} files analyzed", "SUCCESS")
            self._log_activity(f"All files saved in run directory: {RUN_DIR}", "SUCCESS")
            
            return {
                "success": True,
                "framework": self.framework,
                "files_analyzed": len(self.files),
                "test_files_generated": len(test_files),
                "validation_results": validation_results
            }
            
        except Exception as e:
            error_msg = f"Error during test generation: {str(e)}"
            print(f"❌ {error_msg}")
            self._log_activity(error_msg, "ERROR")
            import traceback
            self._log_activity(f"Traceback: {traceback.format_exc()}", "ERROR")
            return {"success": False, "error": str(e)}
        
        finally:
            self._cleanup_temp_directory()
    
    def _clone_repository(self, repo_url: str) -> str:
        """Clone the repository to a temporary directory or use local directory"""
        print(f"🔄 Processing repository: {repo_url}")
        
        # Check if it's a local directory
        if os.path.exists(repo_url) and os.path.isdir(repo_url):
            print(f"📁 Using local directory: {repo_url}")
            self.temp_dir = repo_url
            print(f"✅ Using local directory: {self.temp_dir}")
            return self.temp_dir
        
        # Otherwise, treat it as a GitHub URL and clone it
        print(f"🌐 Cloning GitHub repository: {repo_url}")
        self.temp_dir = tempfile.mkdtemp()
        print(f"ℹ️ Temporary directory: {self.temp_dir}")
        
        try:
            result = subprocess.run(
                ['git', 'clone', repo_url, self.temp_dir],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"📊 Git clone command: {['git', 'clone', repo_url, self.temp_dir]}")
            print(f"✅ Repository cloned successfully to: {self.temp_dir}")
            print(f"📊 Git clone stdout: {result.stdout}")
            print(f"📊 Git clone stderr: {result.stderr}")
            
            return self.temp_dir
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone repository: {e}")
            print(f"📊 Error stdout: {e.stdout}")
            print(f"📊 Error stderr: {e.stderr}")
            raise
    
    def _detect_framework(self) -> str:
        """Detect the frontend framework"""
        print("🔄 Detecting frontend framework")
        
        # Look for package.json files recursively
        package_files = []
        for root, dirs, files in os.walk(self.temp_dir):
            if 'package.json' in files:
                package_files.append(os.path.join(root, 'package.json'))
        
        framework_scores = {'react': 0, 'vue': 0, 'angular': 0, 'svelte': 0}
        
        for package_file in package_files:
            print(f"ℹ️ Found package.json: {package_file}")
            try:
                with open(package_file, 'r') as f:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    dev_dependencies = package_data.get('devDependencies', {})
                    all_deps = {**dependencies, **dev_dependencies}
                    
                    print(f"📊 Dependencies in package.json: {list(all_deps.keys())[:10]}")
                    
                    # Check for framework indicators
                    if 'react' in all_deps:
                        framework_scores['react'] += 1
                        print(f"ℹ️ Found react in package.json -> react")
                    if 'react-dom' in all_deps:
                        framework_scores['react'] += 1
                        print(f"ℹ️ Found react-dom in package.json -> react")
                    if '@types/react' in all_deps:
                        framework_scores['react'] += 1
                        print(f"ℹ️ Found @types/react in package.json -> react")
                    
                    if 'vue' in all_deps:
                        framework_scores['vue'] += 1
                    if '@vue/cli-service' in all_deps:
                        framework_scores['vue'] += 1
                    
                    if '@angular/core' in all_deps:
                        framework_scores['angular'] += 1
                    if '@angular/cli' in all_deps:
                        framework_scores['angular'] += 1
                    
                    if 'svelte' in all_deps:
                        framework_scores['svelte'] += 1
                    if 'svelte-preprocess' in all_deps:
                        framework_scores['svelte'] += 1
                        
            except Exception as e:
                print(f"⚠️ Error reading package.json: {e}")
        
        print(f"📊 Framework detection scores: {framework_scores}")
        print(f"📊 Package files found: {package_files}")
        
        detected_framework = max(framework_scores, key=framework_scores.get)
        if framework_scores[detected_framework] == 0:
            detected_framework = 'unknown'
        
        print(f"✅ Detected framework: {detected_framework}")
        return detected_framework
    
    def _collect_source_files(self) -> List[str]:
        """Collect frontend source files"""
        print("🔄 Collecting frontend source files")
        
        files = []
        extensions = ['.tsx', '.jsx', '.js', '.ts', '.vue', '.html']
        
        for ext in extensions:
            print(f"ℹ️ Scanning for {ext} files")
            for root, dirs, filenames in os.walk(self.temp_dir):
                for filename in filenames:
                    if filename.endswith(ext):
                        file_path = os.path.join(root, filename)
                        file_size = os.path.getsize(file_path)
                        
                        # Skip very large files
                        if file_size > MAX_FILE_SIZE:
                            print(f"⚠️ Skipped {filename} - too large ({file_size} bytes > {MAX_FILE_SIZE})")
                            continue
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                files.append(file_path)
                                print(f"ℹ️ Collected: {filename} ({file_size} bytes, {len(content)} chars)")
                        except Exception as e:
                            print(f"⚠️ Could not read {filename}: {e}")
        
        print(f"✅ File collection complete: {len(files)} files collected")
        return files
    
    def _build_dependency_graph(self, files: List[str]) -> tuple:
        """Build dependency graph and classify files"""
        print("🔄 Building dependency graph and classifying files")
        print(f"ℹ️ Processing {len(files)} files for graph construction")
        
        graph = nx.DiGraph()
        file_roles = {}
        route_map = {}
        
        for file_path in files:
            filename = os.path.basename(file_path)
            print(f"ℹ️ Processing: {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract imports
                imports = self._extract_imports(content)
                print(f"📊 Imports in {filename}: {imports[:5]}")
                
                # Add node to graph
                graph.add_node(filename)
                
                # Add edges for imports
                for imp in imports:
                    if imp.endswith(('.tsx', '.jsx', '.ts', '.js')):
                        target_file = os.path.basename(imp)
                        if target_file in [os.path.basename(f) for f in files]:
                            graph.add_edge(filename, target_file)
                            print(f"ℹ️ Added edge: {filename} -> {target_file}")
                
                # Classify file role
                role = self._classify_file_role(filename, content, imports)
                file_roles[filename] = role
                
                # Extract routes
                routes = self._extract_routes(content)
                if routes:
                    route_map[filename] = routes
                    print(f"ℹ️ Route file: {filename} -> routes: {routes}")
                
                if role == 'Component':
                    print(f"ℹ️ Component file: {filename}")
                elif role == 'API':
                    print(f"ℹ️ API file: {filename}")
                
            except Exception as e:
                print(f"⚠️ Error processing {filename}: {e}")
        
        print(f"✅ Dependency graph built: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
        print(f"📊 File roles distribution: {dict(sorted(file_roles.items(), key=lambda x: x[1]))}")
        print(f"📊 Route mapping: {route_map}")
        return graph, file_roles, route_map
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from file content"""
        imports = []
        
        # Match various import patterns
        patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
            r"require\(['\"]([^'\"]+)['\"]\)",
            r"from\s+['\"]([^'\"]+)['\"]"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
        
        return list(set(imports))
    
    def _classify_file_role(self, filename: str, content: str, imports: List[str]) -> str:
        """Classify file role based on content and imports"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Route files
        if 'route' in filename_lower or 'router' in filename_lower:
            return 'Route'
        
        # API files
        if 'api' in filename_lower or 'service' in filename_lower:
            return 'API'
        
        # Component files
        if any(ext in filename_lower for ext in ['.tsx', '.jsx', '.vue']):
            return 'Component'
        
        # Form files
        if 'form' in filename_lower or 'input' in filename_lower:
            return 'Form'
        
        return 'Other'
    
    def _extract_routes(self, content: str) -> List[str]:
        """Extract route patterns from content"""
        routes = []
        
        # Common route patterns
        patterns = [
            r"path=['\"]([^'\"]+)['\"]",
            r"to=['\"]([^'\"]+)['\"]",
            r"href=['\"]([^'\"]+)['\"]",
            r"Route.*path=['\"]([^'\"]+)['\"]",
            r"navigate\(['\"]([^'\"]+)['\"]\)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            routes.extend(matches)
        
        return list(set(routes))
    
    def _export_graphviz(self, graph: nx.DiGraph, file_roles: Dict[str, str]):
        """Export dependency graph to Graphviz format"""
        print("🔄 Exporting dependency graph to Graphviz format")
        
        dot_content = "digraph CodeDependency {\n"
        dot_content += "  rankdir=TB;\n"
        dot_content += "  node [shape=box, style=filled];\n\n"
        
        # Add nodes with colors based on roles
        role_colors = {
            'Component': 'lightblue',
            'Route': 'lightgreen',
            'API': 'lightcoral',
            'Form': 'lightyellow',
            'Other': 'lightgray'
        }
        
        for node in graph.nodes():
            role = file_roles.get(node, 'Other')
            color = role_colors.get(role, 'lightgray')
            dot_content += f'  "{node}" [fillcolor={color}, label="{node}\\n({role})"];\n'
        
        dot_content += "\n"
        
        # Add edges
        for edge in graph.edges():
            dot_content += f'  "{edge[0]}" -> "{edge[1]}";\n'
        
        dot_content += "}\n"
        
        # Save graphviz file in the run directory
        graphviz_file = os.path.join(RUN_DIR, "code_graph.dot")
        with open(graphviz_file, 'w') as f:
            f.write(dot_content)
        
        print(f"✅ Graphviz export complete: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
        print(f"ℹ️ Graph saved to {graphviz_file}")
        print(f"ℹ️ To visualize: dot -Tpng {graphviz_file} -o {os.path.join(RUN_DIR, 'code_graph.png')}")
    
    def _format_key_pages(self) -> str:
        """Format key pages for the prompt"""
        key_pages = []
        for filename, role in self.file_roles.items():
            if 'Page' in filename and role == 'Component':
                key_pages.append(f"- {filename}")
        return "\n".join(key_pages[:10]) if key_pages else "- No specific pages detected"
    
    def _get_sample_components(self) -> str:
        """Get sample component code for context"""
        sample_components = []
        for file_path in self.files:
            filename = os.path.basename(file_path)
            if self.file_roles.get(filename) == 'Component' and len(sample_components) < 3:
                if 'Page' in filename:  # Prioritize page components
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()[:800]  # First 800 chars
                            sample_components.append(f"{filename}:\n{content[:800]}")
                    except:
                        pass
        return "\n\n".join(sample_components) if sample_components else "No sample components available"
    
    def _build_comprehensive_prompt(self, analysis: Dict[str, Any] = None, user_flows_content: str = "") -> str:
        """Build comprehensive prompt for test generation using advanced analysis"""
        print("🔄 Building comprehensive prompt with advanced analysis")
        
        # Get component information
        component_files = [f for f, role in self.file_roles.items() if role == 'Component']
        api_files = [f for f, role in self.file_roles.items() if role == 'API']
        form_files = [f for f, role in self.file_roles.items() if role == 'Form']
        
        # Use comprehensive analysis if available
        if analysis:
            routes_list = "\n".join([f"- {route}" for route in analysis.get('routes', [])[:15]])
            pages_list = "\n".join([f"- {page}" for page in analysis.get('pages', [])[:15]])
            api_endpoints_list = "\n".join([f"- {endpoint}" for endpoint in analysis.get('api_endpoints', [])[:10]])
            features_list = "\n".join([f"- {feature}" for feature in analysis.get('features', [])])
            user_flows_list = "\n".join([f"- {flow}" for flow in analysis.get('user_flows', [])[:10]])
            sample_routes = analysis.get('routes', [])[:8]
        else:
            # Fallback to basic analysis
            sample_routes = list(set(self.route_map.keys()))[:8]
            routes_list = "\n".join([f"- {route}" for route in sample_routes])
            pages_list = "\n".join([f"- {f}" for f in component_files[:15]])
            api_endpoints_list = "No API endpoints detected"
            features_list = "Basic application functionality"
            user_flows_list = "Standard user flows"
        
        # Get key components list
        key_components_list = "\n".join([f"- {f}" for f in component_files[:15]])
        
        # Get sample component code
        sample_code = self._get_sample_components()
        
        prompt = f"""
You are an expert QA automation engineer. Generate COMPREHENSIVE Playwright tests for this {self.framework.upper()} application.

FRAMEWORK: {self.framework.upper()}

APPLICATION ANALYSIS:
- Total Files: {len(self.files)}
- Components: {len(component_files)}
- API Files: {len(api_files)}
- Form Files: {len(form_files)}
- Routes: {len(self.route_map)}

APPLICATION ROUTES:
{routes_list}

APPLICATION PAGES:
{pages_list}

API ENDPOINTS:
{api_endpoints_list}

APPLICATION FEATURES:
{features_list}

USER FLOWS:
{user_flows_list}

DETAILED USER FLOW DESCRIPTIONS:
{user_flows_content}

KEY COMPONENTS:
{key_components_list}

SAMPLE COMPONENT CODE:
{sample_code}

CRITICAL REQUIREMENTS:
1. **MOST IMPORTANT: Generate tests based EXACTLY on the "DETAILED USER FLOW DESCRIPTIONS" provided above.**
   - Use the specific routes, components, UI elements, and steps from each flow
   - Use the exact button text, input placeholders, and API endpoints mentioned
   - DO NOT generate generic login/authentication tests - use the specific flows provided

2. Generate EXACTLY 4 test files with these EXACT names:
   - visual.spec.ts
   - flow.spec.ts  
   - component.spec.ts
   - accessibility.spec.ts

3. Each file must contain 5-8 COMPREHENSIVE test cases based on the user flows, not basic examples

4. Use this EXACT format for each file:
filename.spec.ts:
```typescript
import {{ test, expect }} from '@playwright/test';

test.describe('Category Name', () => {{
  test('should perform specific comprehensive test', async ({{ page }}) => {{
    await page.goto('/route');
    await page.route('**/api/endpoint', route => route.fulfill({{
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({{ data: 'mock' }})
    }}));
    await expect(page.locator('real-selector')).toBeVisible();
    await page.click('button[data-testid="specific-button"]');
    await expect(page.locator('.result')).toContainText('expected text');
  }});
  
  test('should handle edge case scenario', async ({{ page }}) => {{
    // Detailed edge case testing
  }});
  
  // More comprehensive test cases...
}});
```

4. REQUIREMENTS FOR EACH TEST TYPE:

VISUAL TESTS (visual.spec.ts):
- Test responsive design (mobile 320px, tablet 768px, desktop 1920px)
- Test dark/light theme switching  
- Test loading states and animations
- Test error states and empty states
- Use page.setViewportSize() for different screen sizes
- Test navigation menu visibility on different devices

FLOW TESTS (flow.spec.ts):
**CRITICAL: Generate tests based EXACTLY on the detailed user flows provided above.**
- Test each specific user flow from the "DETAILED USER FLOW DESCRIPTIONS" section
- Use the exact routes, components, UI elements, and steps described in each flow
- Include API mocking for the specific endpoints mentioned in each flow
- Test both success and error paths as described in each flow
- Use the exact button text, input placeholders, and component names from the flows
- DO NOT generate generic login/authentication tests - use the specific flows provided

COMPONENT TESTS (component.spec.ts):
**CRITICAL: Generate tests based on the UI elements and components from the detailed user flows.**
- Test the specific interactive elements mentioned in each user flow
- Use the exact button text, input placeholders, and component names from the flows
- Test form validation and submission as described in the flows
- Test modal open/close behavior for confirmation dialogs mentioned in flows
- Test dropdown selections and filtering functionality from the flows
- Test file upload functionality if mentioned in the flows
- DO NOT generate generic component tests - use the specific UI elements from the flows

ACCESSIBILITY TESTS (accessibility.spec.ts):
- Test ARIA labels and roles on all interactive elements
- Test keyboard navigation (Tab, Enter, Escape)
- Test focus management and focus trapping
- Test screen reader announcements
- Test color contrast and visual indicators
- Ensure all buttons/links are keyboard accessible

5. TECHNICAL REQUIREMENTS:
- Use ES6 imports: import {{ test, expect }} from '@playwright/test'
- Mock ALL API calls with page.route() and realistic JSON responses
- Use realistic selectors: input[type="email"], button[type="submit"], [data-testid="..."]
- Include proper error handling and edge cases
- Use descriptive test names that explain what is being tested
- Include 3-5 assertions per test case minimum
- Test both success and failure scenarios

6. **CRITICAL: Generate REAL, DETAILED tests based EXACTLY on the "DETAILED USER FLOW DESCRIPTIONS" provided above.**
   - Each test should implement one of the specific user flows described
   - Use the exact routes, components, UI elements, button text, and API endpoints from the flows
   - Test both success and error paths as described in each flow
   - DO NOT generate generic login/authentication tests - use the specific flows provided

Generate comprehensive, production-ready test cases now:
"""
        
        print(f"✅ Prompt built successfully ({len(prompt)} characters)")
        
        # Save the full prompt to a file for testing with ChatGPT
        prompt_file = f"{LOG_DIR}/ollama_prompt_{self.run_timestamp}.txt"
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"📝 Full prompt saved to: {prompt_file}")
        
        return prompt
    
    def _ask_ollama_single_file(self, base_prompt: str, test_type: str, test_filename: str) -> str:
        """Generate a single test file with focused prompt"""
        
        # Build focused prompt for single file
        focused_prompt = f"{base_prompt}\n\n**CRITICAL: Generate ONLY {test_filename} with 6-8 comprehensive test cases based on the user flows provided above.**\n\n**REQUIRED OUTPUT FORMAT - COPY THIS EXACTLY:**\n{test_filename}:\n```typescript\nimport {{ test, expect }} from '@playwright/test';\n\n[Your complete test code here - MUST be complete and valid TypeScript]\n```\n\n**IMPORTANT:** \n1. Start your response with exactly: {test_filename}:\n2. Provide COMPLETE TypeScript code in a markdown code block\n3. Use the specific user flows from the DETAILED USER FLOW DESCRIPTIONS above\n4. Include proper imports, test structure, and assertions\n5. Make sure the code is syntactically correct and complete\n6. DO NOT truncate or leave incomplete code"
        
        print(f"🔄 Generating {test_filename} (model: {OLLAMA_MODEL})")
        print(f"ℹ️ Prompt length: {len(focused_prompt)} characters")
        self._log_activity(f"Generating {test_filename} with {len(focused_prompt)} character prompt")
        
        # Save individual file prompt to logs
        individual_prompt_file = f"{LOG_DIR}/ollama_prompt_{self.run_timestamp}_{test_filename.replace('.spec.ts', '')}.txt"
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(individual_prompt_file, 'w', encoding='utf-8') as f:
            f.write(focused_prompt)
        print(f"📝 Individual prompt saved to: {individual_prompt_file}")
        self._log_activity(f"Individual prompt saved: {individual_prompt_file}")
        
        request_data = {
            'model': OLLAMA_MODEL,
            'prompt': focused_prompt,
            'stream': False,
            'options': {
                'num_predict': 5000,  # Increased for complete test files
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40
            }
        }
        
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                print(f"✅ Generated {test_filename}: {len(response_text)} characters")
                self._log_activity(f"Generated {test_filename}: {len(response_text)} characters")
                
                # Save response to logs
                response_file = f"{LOG_DIR}/ollama_response_{self.run_timestamp}_{test_filename.replace('.spec.ts', '')}.txt"
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(response_text)
                print(f"📝 Response saved to: {response_file}")
                self._log_activity(f"Response saved: {response_file}")
                
                return response_text
            else:
                error_msg = f"Ollama request failed: {response.status_code}"
                print(f"❌ {error_msg}")
                self._log_activity(error_msg, "ERROR")
                return ""
        except Exception as e:
            error_msg = f"Error calling Ollama: {e}"
            print(f"❌ {error_msg}")
            self._log_activity(error_msg, "ERROR")
            return ""
    
    def _ask_ollama(self, prompt: str) -> str:
        """Send prompt to Ollama and get response - generates one file at a time"""
        print(f"🔄 Sending prompts to Ollama (model: {OLLAMA_MODEL})")
        print(f"ℹ️ Base prompt length: {len(prompt)} characters")
        print("ℹ️ Strategy: Generating each test file individually for better quality")
        
        # Save base prompt
        prompt_file = f"{LOG_DIR}/ollama_base_prompt_{self.run_timestamp}.txt"
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"📝 Base prompt saved to: {prompt_file}")
        
        # Generate each file individually
        test_files = [
            ('visual.spec.ts', 'Visual Tests'),
            ('flow.spec.ts', 'User Flow Tests'),
            ('component.spec.ts', 'Component Interaction Tests'),
            ('accessibility.spec.ts', 'Accessibility Tests')
        ]
        
        combined_response = ""
        for filename, description in test_files:
            print(f"\n{'='*60}")
            print(f"📝 Generating: {filename} ({description})")
            print(f"{'='*60}")
            
            file_response = self._ask_ollama_single_file(prompt, description, filename)
            if file_response:
                # Add to combined response with clear separator
                combined_response += f"\n\n{filename}:\n{file_response}\n"
            else:
                print(f"⚠️ Warning: Failed to generate {filename}")
        
        print(f"\n{'='*60}")
        print(f"✅ All files generated: {len(combined_response)} total characters")
        print(f"{'='*60}")
        
        return combined_response
    
    def _parse_test_files(self, response_text: str) -> List[str]:
        """Parse test files from Ollama response"""
        print("🔄 Parsing and saving test files from Ollama response")
        print(f"📊 Raw test response: {response_text[:500]}...")
        
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        files_saved = []
        
        print(f"ℹ️ Processing {len(response_text.splitlines())} lines of response")
        
        # Try multiple parsing strategies
        files_saved.extend(self._parse_filename_format(response_text))
        files_saved.extend(self._parse_hash_format(response_text))
        files_saved.extend(self._parse_markdown_format(response_text))
        
        # If we still don't have the expected files, try to map based on content
        if len(files_saved) < 4:
            files_saved.extend(self._parse_by_content_mapping(response_text))
        
        # Remove duplicates while preserving order
        files_saved = list(dict.fromkeys(files_saved))
        
        print(f"✅ Test file parsing complete: {len(files_saved)} files saved")
        print(f"📊 Files saved: {files_saved}")
        
        if not files_saved:
            print("❌ No test files were generated!")
            print("⚠️ Response might not contain properly formatted test files")
            print(f"📊 Response analysis: {{'total_lines': {len(response_text.splitlines())}, 'contains_spec': {'.spec.ts' in response_text}, 'contains_comments': {'//' in response_text}, 'contains_backticks': {'```' in response_text}, 'response_preview': '{response_text[:1000]}'}}")
        
        return files_saved
    
    def _parse_filename_format(self, response_text: str) -> List[str]:
        """Parse FILENAME: format"""
        files_saved = []
        filename_pattern = r'FILENAME:\s*(\S+\.spec\.ts)\s*\n(.*?)(?=FILENAME:|$)'
        matches = re.findall(filename_pattern, response_text, re.DOTALL)
        
        for filename, content in matches:
            content = content.strip()
            if content:
                if self._save_file(filename, content):
                    files_saved.append(filename)
                    print(f"✅ Found test file marker: {filename}")
        
        return files_saved
    
    def _parse_hash_format(self, response_text: str) -> List[str]:
        """Parse #### filename.spec.ts format"""
        files_saved = []
        hash_pattern = r'####\s*(\S+\.spec\.ts)\s*\n```typescript\s*\n(.*?)\n```'
        hash_matches = re.findall(hash_pattern, response_text, re.DOTALL)
        
        for filename, content in hash_matches:
            content = content.strip()
            if content:
                if self._save_file(filename, content):
                    files_saved.append(filename)
                    print(f"✅ Found test file marker: {filename}")
        
        return files_saved
    
    def _parse_markdown_format(self, response_text: str) -> List[str]:
        """Parse markdown code blocks with filename extraction"""
        files_saved = []
        
        # Strategy 1: Look for filename.spec.ts: followed by markdown code block
        filename_pattern = r'(\w+\.spec\.ts):\s*\n```typescript\s*\n(.*?)\n```'
        matches = re.findall(filename_pattern, response_text, re.DOTALL)
        
        for filename, content in matches:
            content = content.strip()
            if content:
                if self._save_file(filename, content):
                    files_saved.append(filename)
                    print(f"✅ Found test file marker: {filename}")
        
        # Strategy 2: Look for markdown blocks and try to extract filename from context
        if not files_saved:
            markdown_blocks = re.findall(r'```(?:typescript|javascript|ts|js)\s*\n(.*?)\n```', response_text, re.DOTALL)
            
            for i, block_content in enumerate(markdown_blocks):
                # Try to find filename in the text before the code block
                lines_before = response_text[:response_text.find(block_content)].split('\n')
                filename = None
                
                # Look for filename patterns in the preceding lines
                for line in reversed(lines_before[-10:]):  # Check last 10 lines
                    if '.spec.ts' in line:
                        # Extract filename from line
                        match = re.search(r'(\w+\.spec\.ts)', line)
                        if match:
                            filename = match.group(1)
                            break
                
                # Fallback to generic name if no filename found
                if not filename:
                    filename = f"test_{i+1}.spec.ts"
                
                content = block_content.strip()
                if content:
                    if self._save_file(filename, content):
                        files_saved.append(filename)
                        print(f"✅ Found test file marker: {filename}")
        
        return files_saved
    
    def _parse_by_content_mapping(self, response_text: str) -> List[str]:
        """Parse by mapping content to expected filenames based on test content"""
        files_saved = []
        
        # Expected filenames and their content indicators
        expected_files = {
            'visual.spec.ts': ['visual', 'responsive', 'viewport', 'theme', 'dark', 'light', 'mobile', 'desktop'],
            'flow.spec.ts': ['flow', 'login', 'navigation', 'user', 'authentication', 'wizard', 'form'],
            'component.spec.ts': ['component', 'interactive', 'button', 'modal', 'dropdown', 'form', 'input'],
            'accessibility.spec.ts': ['accessibility', 'aria', 'keyboard', 'focus', 'screen reader', 'tab']
        }
        
        # Find all code blocks
        markdown_blocks = re.findall(r'```(?:typescript|javascript|ts|js)\s*\n(.*?)\n```', response_text, re.DOTALL)
        
        for i, block_content in enumerate(markdown_blocks):
            content_lower = block_content.lower()
            
            # Find the best matching filename based on content
            best_match = None
            best_score = 0
            
            for filename, indicators in expected_files.items():
                score = sum(1 for indicator in indicators if indicator in content_lower)
                if score > best_score:
                    best_score = score
                    best_match = filename
            
            # Use the best match or fallback to generic name
            filename = best_match if best_match else f"test_{i+1}.spec.ts"
            
            content = block_content.strip()
            if content:
                if self._save_file(filename, content):
                    files_saved.append(filename)
                    print(f"✅ Mapped content to: {filename}")
        
        return files_saved
    
    def _analyze_application_functionality(self) -> Dict[str, Any]:
        """Perform comprehensive application analysis to understand full functionality"""
        print("🔍 Performing comprehensive application analysis")
        
        analysis = {
            "routes": [],
            "components": [],
            "pages": [],
            "forms": [],
            "api_endpoints": [],
            "user_flows": [],
            "features": []
        }
        
        # Analyze all files for functionality
        for file_path in self.files:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract routes
                route_matches = re.findall(r'["\']([^"\']*\/[^"\']*)["\']', content)
                for route in route_matches:
                    if route.startswith('/') and route not in analysis["routes"]:
                        analysis["routes"].append(route)
                
                # Extract components and pages
                if any(keyword in filename.lower() for keyword in ['page', 'component', 'view', 'screen']):
                    analysis["pages"].append(filename)
                
                # Extract forms
                if 'form' in content.lower() or 'Form' in filename:
                    analysis["forms"].append(filename)
                
                # Extract API calls
                api_patterns = [
                    r'fetch\(["\']([^"\']+)["\']',
                    r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']',
                    r'api\.([^"\']+)',
                    r'\/api\/[^"\'\s]+'
                ]
                for pattern in api_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if isinstance(match, tuple):
                            endpoint = match[1] if len(match) > 1 else match[0]
                        else:
                            endpoint = match
                        if endpoint.startswith('/api/') and endpoint not in analysis["api_endpoints"]:
                            analysis["api_endpoints"].append(endpoint)
                
                # Extract user flows from component names and content
                if any(keyword in filename.lower() for keyword in ['login', 'signup', 'dashboard', 'profile', 'settings', 'create', 'edit', 'delete']):
                    analysis["user_flows"].append(filename)
                
            except Exception as e:
                print(f"⚠️ Error analyzing {filename}: {e}")
        
        # Generate feature analysis
        analysis["features"] = self._extract_features(analysis)
        
        print(f"📊 Analysis complete: {len(analysis['routes'])} routes, {len(analysis['pages'])} pages, {len(analysis['api_endpoints'])} APIs")
        
        return analysis
    
    def _generate_user_flows_report(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive User Flow Description Report using LLM"""
        print("🔄 Generating User Flow Description Report")
        
        # Extract context for the prompt
        routes_list = "\n".join([f"- {route}" for route in analysis.get('routes', [])[:20]])
        components_list = "\n".join([f"- {comp}" for comp in analysis.get('pages', [])[:20]])
        api_endpoints_list = "\n".join([f"- {endpoint}" for endpoint in analysis.get('api_endpoints', [])[:15]])
        
        # Get detailed component analysis
        component_details = self._analyze_component_details()
        form_analysis = self._analyze_form_components()
        ui_elements_analysis = self._analyze_ui_elements()
        
        # Build the enhanced user flow generation prompt
        user_flow_prompt = f"""You are a senior QA automation architect analyzing a frontend codebase for test generation purposes. Your task is to generate **SPECIFIC User Flows** based on the provided routes, components, and APIs.

IMPORTANT: This is for automated test generation. You MUST analyze the provided codebase context and generate flows based on the actual components and routes listed below.

CRITICAL REQUIREMENTS:
- **ANALYZE THE PROVIDED CODEBASE** - Use the exact routes, components, and APIs provided below
- **Generate specific flows** based on the real application components
- **Use exact names** from the routes, components, and API endpoints listed
- **Generate 8-15 distinct flows** covering different application features
- **Exclude authentication flows** (login, register, password reset)
- **Focus on business logic** and application-specific functionality

Here is the analyzed codebase context:

ROUTES FOUND:
{routes_list}

COMPONENTS DETECTED:
{components_list}

API ENDPOINTS:
{api_endpoints_list}

DETAILED COMPONENT ANALYSIS:
{component_details}

FORM COMPONENTS ANALYSIS:
{form_analysis}

UI ELEMENTS ANALYSIS:
{ui_elements_analysis}

IMPORTANT INSTRUCTIONS:
1. **DETAILED ANALYSIS REQUIRED**: Examine each component's actual functionality, not just names
2. **SPECIFIC UI ELEMENTS**: Include exact button text, form field names, modal titles, etc.
3. **INTERACTION SEQUENCES**: Describe precise user actions and system responses
4. **STATE MANAGEMENT**: Include loading states, validation states, error states
5. **EDGE CASES**: Cover error scenarios, empty states, validation failures
6. **EXCLUDE BASIC AUTH**: Do NOT generate login, registration, or password reset flows
7. **FOCUS ON BUSINESS LOGIC**: Prioritize application-specific features and workflows
8. **COMPREHENSIVE COVERAGE**: Generate 8-15 distinct user flows based on actual functionality

OUTPUT FORMAT - Generate detailed flows using this structure:

---
## Flow: [Flow Name Based on Actual Components]

- **Route**: [Actual route from the routes list above]
- **Components**: [Actual component names from the components list above]
- **UI Elements**:
  - [Specific UI elements found in the actual components]
  - [Button text, form fields, modal titles from actual code]
  - [Input placeholders, dropdown options from actual code]
- **Steps**:
  1. [Specific user action based on actual component functionality]
  2. [System response based on actual component behavior]
  3. [Next user action based on actual UI elements]
  4. [Validation/error handling based on actual form components]
  5. [Navigation/API calls based on actual routes and endpoints]

**CRITICAL REQUIREMENTS**:
- Use ONLY the routes, components, and API endpoints listed above
- Generate flows based on the ACTUAL application functionality
- Do NOT use generic examples - analyze the real codebase
- Focus on security, compliance, and analysis features (not project management)
- Use exact component names like SecurityIntelligenceDashboard, AgentsDashboard, etc.
- Generate 8-15 distinct flows covering different application features
- Exclude authentication flows (login, registration, password reset)

**ANALYZE THE ACTUAL COMPONENTS**:
Look at the component names and infer their functionality:
- SecurityIntelligenceDashboard → Security analysis and intelligence features
- AgentsDashboard → AI agent management and monitoring
- ApplicationCard/ApplicationDetailsView → Application management
- Compliance → Compliance checking and reporting
- Integrations → Third-party integrations
- GitHubIntegrationCard → GitHub integration features
- CyberNewsCard → Security news and updates
- HazardRow/BlastRadiusRow → Security risk analysis
- RemediationAgentCard → Security remediation workflows

**CRITICAL**: Generate flows based on the ACTUAL routes and components provided above. Use the exact names and create realistic user interactions. Do NOT provide generic advice - analyze the real codebase and generate specific flows."""
        
        print(f"🔄 Sending user flow generation prompt to Ollama (model: {OLLAMA_MODEL})")
        print(f"ℹ️ Prompt length: {len(user_flow_prompt)} characters")
        
        # Save the prompt for debugging
        prompt_file = f"{LOG_DIR}/user_flow_prompt_{self.run_timestamp}.txt"
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(user_flow_prompt)
        print(f"📝 User flow prompt saved: {prompt_file}")
        
        # Call Ollama API
        request_data = {
            'model': OLLAMA_MODEL,
            'prompt': user_flow_prompt,
            'stream': False,
            'options': {
                'num_predict': 2000,
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40
            }
        }
        
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                user_flows_content = result.get('response', '')
                print(f"✅ Generated user flows report: {len(user_flows_content)} characters")
                
                # Save the user flows report
                self._save_user_flows_report(user_flows_content)
                
                return user_flows_content
            else:
                print(f"❌ Ollama request failed: {response.status_code}")
                return ""
        except Exception as e:
            print(f"❌ Error calling Ollama for user flows: {e}")
            return ""
    
    def _save_user_flows_report(self, content: str) -> None:
        """Save user flows report to reports directory"""
        try:
            os.makedirs(REPORT_DIR, exist_ok=True)
            report_path = os.path.join(REPORT_DIR, "user_flows.md")
            
            # Add header to the report
            report_content = f"""# User Flow Description Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Repository: {self.temp_dir}

This report describes the distinct user flows identified in the application based on route analysis, component structure, and API usage patterns.

---

{content}

---

*Report generated by AI Playwright Test Generator*
"""
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"✅ User flows report saved: {report_path}")
        except Exception as e:
            print(f"❌ Error saving user flows report: {e}")
    
    def _analyze_component_details(self) -> str:
        """Analyze component files to extract detailed UI information"""
        print("🔍 Analyzing component details for UI elements")
        
        component_details = []
        
        for file_path in self.files:
            filename = os.path.basename(file_path)
            if self.file_roles.get(filename) == 'Component':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract component information
                    details = self._extract_component_info(filename, content)
                    if details:
                        component_details.append(details)
                        
                except Exception as e:
                    print(f"⚠️ Error analyzing component {filename}: {e}")
        
        return "\n".join(component_details[:15]) if component_details else "No detailed component analysis available"
    
    def _extract_component_info(self, filename: str, content: str) -> str:
        """Extract detailed information from a component file"""
        info_parts = [f"**{filename}**:"]
        
        # Extract form elements
        form_elements = []
        input_patterns = [
            r'<input[^>]*type=["\']([^"\']*)["\'][^>]*placeholder=["\']([^"\']*)["\'][^>]*>',
            r'<input[^>]*placeholder=["\']([^"\']*)["\'][^>]*type=["\']([^"\']*)["\'][^>]*>',
            r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>',
            r'<textarea[^>]*placeholder=["\']([^"\']*)["\'][^>]*>',
            r'<select[^>]*>',
            r'<button[^>]*>([^<]*)</button>'
        ]
        
        for pattern in input_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    form_elements.append(f"  - {match[0]}: {match[1] if len(match) > 1 else 'field'}")
                else:
                    form_elements.append(f"  - {match}")
        
        if form_elements:
            info_parts.append("  Form Elements:")
            info_parts.extend(form_elements[:5])  # Limit to 5 elements
        
        # Extract API calls
        api_calls = re.findall(r'(?:fetch|axios|api)\(["\']([^"\']+)["\']', content)
        if api_calls:
            info_parts.append("  API Calls:")
            for api in api_calls[:3]:  # Limit to 3 API calls
                info_parts.append(f"    - {api}")
        
        # Extract state management
        state_patterns = [
            r'useState\(["\']([^"\']*)["\']',
            r'setState\(["\']([^"\']*)["\']',
            r'const\s+(\w+)\s*=\s*useState'
        ]
        
        states = []
        for pattern in state_patterns:
            matches = re.findall(pattern, content)
            states.extend(matches)
        
        if states:
            info_parts.append("  State Variables:")
            for state in states[:3]:  # Limit to 3 states
                info_parts.append(f"    - {state}")
        
        return "\n".join(info_parts) if len(info_parts) > 1 else ""
    
    def _analyze_form_components(self) -> str:
        """Analyze form components specifically"""
        print("🔍 Analyzing form components")
        
        form_details = []
        
        for file_path in self.files:
            filename = os.path.basename(file_path)
            if 'form' in filename.lower() or self.file_roles.get(filename) == 'Form':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    form_info = self._extract_form_details(filename, content)
                    if form_info:
                        form_details.append(form_info)
                        
                except Exception as e:
                    print(f"⚠️ Error analyzing form {filename}: {e}")
        
        return "\n".join(form_details[:10]) if form_details else "No form components detected"
    
    def _extract_form_details(self, filename: str, content: str) -> str:
        """Extract detailed form information"""
        form_parts = [f"**{filename}**:"]
        
        # Extract form fields with validation
        field_patterns = [
            r'<input[^>]*name=["\']([^"\']*)["\'][^>]*required[^>]*>',
            r'<input[^>]*required[^>]*name=["\']([^"\']*)["\'][^>]*>',
            r'<textarea[^>]*name=["\']([^"\']*)["\'][^>]*>',
            r'<select[^>]*name=["\']([^"\']*)["\'][^>]*>'
        ]
        
        fields = []
        for pattern in field_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            fields.extend(matches)
        
        if fields:
            form_parts.append("  Required Fields:")
            for field in fields[:5]:
                form_parts.append(f"    - {field}")
        
        # Extract validation rules
        validation_patterns = [
            r'minLength[=:]\s*(\d+)',
            r'maxLength[=:]\s*(\d+)',
            r'pattern[=:]\s*["\']([^"\']*)["\']',
            r'required[=:]\s*true'
        ]
        
        validations = []
        for pattern in validation_patterns:
            matches = re.findall(pattern, content)
            validations.extend(matches)
        
        if validations:
            form_parts.append("  Validation Rules:")
            for validation in validations[:3]:
                form_parts.append(f"    - {validation}")
        
        # Extract submit handlers
        submit_patterns = [
            r'onSubmit[=:]\s*{([^}]+)}',
            r'handleSubmit[=:]\s*{([^}]+)}',
            r'submit[=:]\s*{([^}]+)}'
        ]
        
        submit_handlers = []
        for pattern in submit_patterns:
            matches = re.findall(pattern, content)
            submit_handlers.extend(matches)
        
        if submit_handlers:
            form_parts.append("  Submit Handlers:")
            for handler in submit_handlers[:2]:
                form_parts.append(f"    - {handler[:50]}...")
        
        return "\n".join(form_parts) if len(form_parts) > 1 else ""
    
    def _analyze_ui_elements(self) -> str:
        """Analyze UI elements across all components"""
        print("🔍 Analyzing UI elements and interactions")
        
        ui_elements = {
            'buttons': [],
            'modals': [],
            'navigation': [],
            'dropdowns': [],
            'tables': [],
            'cards': []
        }
        
        for file_path in self.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract buttons
                button_matches = re.findall(r'<button[^>]*>([^<]*)</button>', content, re.IGNORECASE)
                ui_elements['buttons'].extend([btn.strip() for btn in button_matches if btn.strip()])
                
                # Extract modals
                modal_matches = re.findall(r'(?:Modal|Dialog|Popup)[^>]*title=["\']([^"\']*)["\']', content, re.IGNORECASE)
                ui_elements['modals'].extend(modal_matches)
                
                # Extract navigation
                nav_matches = re.findall(r'<nav[^>]*>([^<]*)</nav>', content, re.IGNORECASE)
                ui_elements['navigation'].extend([nav.strip() for nav in nav_matches if nav.strip()])
                
                # Extract dropdowns
                dropdown_matches = re.findall(r'<select[^>]*>', content, re.IGNORECASE)
                ui_elements['dropdowns'].extend(dropdown_matches)
                
                # Extract tables
                table_matches = re.findall(r'<table[^>]*>', content, re.IGNORECASE)
                ui_elements['tables'].extend(table_matches)
                
                # Extract cards
                card_matches = re.findall(r'(?:Card|Panel|Box)[^>]*>', content, re.IGNORECASE)
                ui_elements['cards'].extend(card_matches)
                
            except Exception as e:
                print(f"⚠️ Error analyzing UI elements in {file_path}: {e}")
        
        # Format UI elements analysis
        analysis_parts = []
        for element_type, elements in ui_elements.items():
            if elements:
                analysis_parts.append(f"**{element_type.title()}**:")
                for element in elements[:5]:  # Limit to 5 per type
                    analysis_parts.append(f"  - {element}")
                analysis_parts.append("")
        
        return "\n".join(analysis_parts) if analysis_parts else "No specific UI elements detected"
    
    def _extract_features(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract application features from analysis"""
        features = []
        
        # Dashboard features
        if any('dashboard' in route.lower() or 'dashboard' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Dashboard Management")
        
        # CRUD operations
        if any('create' in route.lower() or 'create' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Create Operations")
        if any('edit' in route.lower() or 'edit' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Edit Operations")
        if any('delete' in route.lower() or 'delete' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Delete Operations")
        
        # Project management
        if any('project' in route.lower() or 'project' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Project Management")
        
        # User management
        if any('user' in route.lower() or 'profile' in route.lower() for route in analysis["routes"]):
            features.append("User Management")
        
        # Content management
        if any('content' in route.lower() or 'content' in page.lower() for route in analysis["routes"] for page in analysis["pages"]):
            features.append("Content Management")
        
        # File management
        if any('file' in route.lower() or 'upload' in route.lower() or 'download' in route.lower() for route in analysis["routes"]):
            features.append("File Management")
        
        # Search and filtering
        if any('search' in route.lower() or 'filter' in route.lower() for route in analysis["routes"]):
            features.append("Search and Filtering")
        
        # Settings and configuration
        if any('setting' in route.lower() or 'config' in route.lower() for route in analysis["routes"]):
            features.append("Settings and Configuration")
        
        # E-commerce features
        if any('cart' in route.lower() or 'checkout' in route.lower() or 'order' in route.lower() for route in analysis["routes"]):
            features.append("E-commerce")
        
        # Blog/content features
        if any('blog' in route.lower() or 'post' in route.lower() or 'article' in route.lower() for route in analysis["routes"]):
            features.append("Blog/Content Publishing")
        
        # Analytics and reporting
        if any('analytics' in route.lower() or 'report' in route.lower() or 'stats' in route.lower() for route in analysis["routes"]):
            features.append("Analytics and Reporting")
        
        # Communication features
        if any('message' in route.lower() or 'chat' in route.lower() or 'notification' in route.lower() for route in analysis["routes"]):
            features.append("Communication")
        
        # Calendar/scheduling
        if any('calendar' in route.lower() or 'schedule' in route.lower() or 'event' in route.lower() for route in analysis["routes"]):
            features.append("Calendar/Scheduling")
        
        return features
    
    def _generate_comprehensive_report(self, analysis: Dict[str, Any], validation_results: Dict[str, Any]) -> str:
        """Generate comprehensive analysis report"""
        print("📝 Generating comprehensive analysis report")
        
        report = f"""
# Application Analysis Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Repository: {self.temp_dir}

## Framework Detection
- **Framework**: {self.framework}
- **Total Files Analyzed**: {len(self.files)}

## Application Structure
### Routes ({len(analysis['routes'])})
{chr(10).join([f"- {route}" for route in analysis['routes'][:20]])}

### Pages/Components ({len(analysis['pages'])})
{chr(10).join([f"- {page}" for page in analysis['pages'][:20]])}

### API Endpoints ({len(analysis['api_endpoints'])})
{chr(10).join([f"- {endpoint}" for endpoint in analysis['api_endpoints'][:20]])}

### Forms ({len(analysis['forms'])})
{chr(10).join([f"- {form}" for form in analysis['forms'][:10]])}

## Application Features
{chr(10).join([f"- {feature}" for feature in analysis['features']])}

## User Flows Identified
{chr(10).join([f"- {flow}" for flow in analysis['user_flows'][:15]])}

## File Roles Classification
{chr(10).join([f"- {filename}: {role}" for filename, role in list(self.file_roles.items())[:20]])}

## Test Generation Recommendations
Based on the analysis, the following test scenarios should be prioritized:

### Visual Tests
- Responsive design testing across all identified routes
- Theme switching (if applicable)
- Loading states and error handling

### User Flow Tests
- Authentication flow (login/logout)
- Navigation between all major pages
- CRUD operations for identified features
- Form submissions and validations

### Component Tests
- Interactive elements testing
- Modal and dropdown functionality
- Form validation and submission
- Data display and filtering

### Accessibility Tests
- Keyboard navigation
- Screen reader compatibility
- ARIA labels and roles
- Focus management

## Test Generation Results
- **Test Files Generated**: {validation_results['total_tests']}
- **Valid Tests**: {validation_results['valid_tests']}/{validation_results['total_tests']}
- **Invalid Tests**: {validation_results['invalid_tests']}
- **Validation Errors**: {len(validation_results['validation_errors'])}

## Technical Details
- **Max File Size**: {MAX_FILE_SIZE} bytes
- **Analysis Depth**: Comprehensive
- **Framework**: {self.framework}
- **Total Components**: {len([f for f, r in self.file_roles.items() if r == 'Component'])}

---
Report generated by AI Playwright Test Generator
"""
        
        return report
    
    def _save_report(self, report: str) -> None:
        """Save comprehensive report to reports directory"""
        try:
            os.makedirs(REPORT_DIR, exist_ok=True)
            report_filename = f"analysis_report_{self.run_timestamp}.md"
            report_path = os.path.join(REPORT_DIR, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ Comprehensive report saved: {report_path}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def _is_valid_test_content(self, content: str) -> bool:
        """Validate that test content is complete and valid"""
        if not content or len(content.strip()) < 100:
            return False
        
        # Check for basic test structure
        has_imports = "import { test, expect }" in content
        has_tests = "test(" in content or "test.describe" in content
        has_closing = content.count('{') == content.count('}')  # Basic bracket matching
        
        return has_imports and has_tests and has_closing
    
    def _save_file(self, filename: str, content: str) -> bool:
        """Save test file to disk"""
        try:
            file_path = os.path.join(TEST_OUTPUT_DIR, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"ℹ️ Saving file: {filename} ({len(content)} characters)")
            print(f"📊 File Content - {filename}: {content[:100]}...")
            print(f"✅ Generated: {TEST_OUTPUT_DIR}/{filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
            return False
    
    def _validate_tests(self, test_files: List[str]) -> Dict[str, Any]:
        """Validate generated test files"""
        validation_results = {
            "total_tests": 0,
            "valid_tests": 0,
            "invalid_tests": 0,
            "validation_errors": []
        }
        
        for test_file in test_files:
            try:
                with open(f"{TEST_OUTPUT_DIR}/{test_file}", 'r') as f:
                    content = f.read()
                    # Basic validation - check for Playwright imports and test structure
                    if "import { test, expect }" in content and ("test.describe" in content or "test('" in content):
                        validation_results["valid_tests"] += 1
                    else:
                        validation_results["invalid_tests"] += 1
                        validation_results["validation_errors"].append(f"Invalid test structure in {test_file}")
            except Exception as e:
                validation_results["invalid_tests"] += 1
                validation_results["validation_errors"].append(f"Error reading {test_file}: {str(e)}")
        
        validation_results["total_tests"] = validation_results["valid_tests"] + validation_results["invalid_tests"]
        return validation_results
    
    def _format_file_roles_distribution(self) -> str:
        """Format file roles distribution for report"""
        role_counts = {}
        for role in self.file_roles.values():
            role_counts[role] = role_counts.get(role, 0) + 1
        
        formatted = ""
        for role, count in role_counts.items():
            formatted += f"- **{role}**: {count} files\n"
        return formatted
    
    def _format_api_analysis(self) -> str:
        """Format API analysis for report"""
        formatted = ""
        for file, routes in self.route_map.items():
            for route in routes:
                formatted += f"- **{route}**: GET\n"
        return formatted
    
    def _format_selector_analysis(self) -> str:
        """Format selector analysis for report"""
        return "- **other**: 304 selectors\n"
    
    def _format_test_files(self, validation_results: Dict[str, Any]) -> str:
        """Format test files for report"""
        formatted = ""
        for i in range(validation_results['total_tests']):
            formatted += f"- **test_{i+1}.spec.ts**: Test file\n"
        return formatted
    
    def _format_validation_errors(self, validation_results: Dict[str, Any]) -> str:
        """Format validation errors for report"""
        formatted = ""
        for error in validation_results.get('validation_errors', []):
            formatted += f"- Error reading {error}\n"
        return formatted
    
    def _cleanup_temp_directory(self):
        """Clean up temporary directory (only if it was created by git clone)"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                # Only clean up if it's a temporary directory (created by tempfile.mkdtemp())
                # Don't delete local directories that were passed as input
                if self.temp_dir.startswith('/tmp') or self.temp_dir.startswith('/var/folders'):
                    import shutil
                    shutil.rmtree(self.temp_dir)
                    print(f"🧹 Cleaned up temporary directory: {self.temp_dir}")
                else:
                    print(f"ℹ️ Preserving local directory: {self.temp_dir}")
            except Exception as e:
                print(f"⚠️ Could not clean up temporary directory: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python integrated_test_generator.py <repository_url_or_local_path>")
        print("  Examples:")
        print("    python integrated_test_generator.py https://github.com/facebook/react")
        print("    python integrated_test_generator.py /path/to/local/project")
        print("    python integrated_test_generator.py ./my-react-app")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    # Create a single timestamp for this run
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    generator = IntegratedTestGenerator(run_timestamp=run_timestamp)
    
    result = generator.generate_tests(repo_url)
    
    if result["success"]:
        print("\n🎉 Test generation completed successfully!")
        print(f"Generated {result['test_files_generated']} test files")
    else:
        print(f"\n❌ Test generation failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
