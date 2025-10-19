# User Flow Description Report Feature

## Overview

The User Flow Description Report is a new feature in the AI Playwright Test Generator that analyzes frontend codebases and generates comprehensive user flow descriptions using LLM (Ollama). This report serves as a reference for generating targeted Playwright tests.

## How It Works

### 1. Analysis Phase
The system performs comprehensive analysis of the codebase to extract:
- **Routes**: All application routes (e.g., `/login`, `/dashboard`, `/profile`)
- **Components**: Detected React/Vue/Angular components from the dependency graph
- **API Endpoints**: API calls found in the codebase (e.g., `/api/auth/login`)

### 2. User Flow Generation
Using the extracted context, the system sends a specialized prompt to Ollama (codellama:instruct) to generate detailed user flows that describe:
- Real-world user interactions
- Step-by-step flow descriptions
- Component involvement
- API call references
- Error handling scenarios

### 3. Report Output
The generated user flows are saved to `./reports/user_flows.md` with:
- Timestamp and repository information
- Detailed flow descriptions
- Structured format for easy reference

## Integration with Test Generation

The user flows are integrated into the test generation pipeline:

1. **Step 5.5**: Comprehensive application analysis
2. **Step 5.6**: User Flow Description Report generation ← **NEW**
3. **Step 6**: Test generation using user flows as context

## Example User Flow Output

```markdown
## Flow: User Login

- Route: /login
- Components: LoginForm, AuthLayout
- Steps:
  1. User visits /login
  2. Enters email and password
  3. Clicks "Login" button
  4. App calls POST /api/login
  5. On success: redirect to /dashboard
  6. On failure: show error message

## Flow: Project Creation

- Route: /projects/create
- Components: ProjectForm, ProjectLayout
- Steps:
  1. User navigates to /projects/create
  2. Fills project form with name, description, and settings
  3. Clicks "Create Project" button
  4. App calls POST /api/projects/create
  5. On success: redirect to /projects with success message
  6. On validation error: show field-specific error messages
```

## Benefits

1. **Comprehensive Coverage**: Identifies all major user flows in the application
2. **Test Context**: Provides rich context for generating realistic test scenarios
3. **Documentation**: Creates valuable documentation of application behavior
4. **Quality Assurance**: Ensures tests cover real user interactions, not just technical scenarios

## Technical Implementation

### Key Methods Added

- `_generate_user_flows_report()`: Main method for generating user flows
- `_save_user_flows_report()`: Saves the report to disk
- Updated `_build_comprehensive_prompt()`: Includes user flows in test generation

### Configuration

The feature uses the same Ollama configuration as the main test generation:
- Model: `codellama:instruct` (configurable via `OLLAMA_MODEL` env var)
- API URL: `http://localhost:11434/api/generate` (configurable via `OLLAMA_API_URL`)

### Output Location

- Report saved to: `./reports/user_flows.md`
- Directory created automatically if it doesn't exist

## Usage

The feature is automatically integrated into the main test generation pipeline. When you run:

```bash
python integrated_test_generator.py <repository_url>
```

The system will:
1. Clone and analyze the repository
2. Generate the User Flow Description Report
3. Use the flows to generate comprehensive Playwright tests

## Testing

A test script is provided to demonstrate the functionality:

```bash
python test_user_flows.py
```

This script uses mock analysis data to test the user flow generation without requiring a full repository clone.

## Future Enhancements

Potential improvements for the User Flow Description Report:

1. **Flow Prioritization**: Rank flows by importance/frequency
2. **Edge Case Detection**: Identify error scenarios and edge cases
3. **Flow Dependencies**: Map relationships between different flows
4. **Visual Flow Diagrams**: Generate Mermaid diagrams for flow visualization
5. **Custom Flow Templates**: Allow users to define custom flow patterns

## Troubleshooting

### Common Issues

1. **Ollama Not Running**: Ensure Ollama is running on the configured URL
2. **Empty Flows**: Check that routes and components are properly detected
3. **Report Not Saved**: Verify write permissions to the `reports` directory

### Debug Information

The system provides detailed logging for troubleshooting:
- Analysis results (routes, components, APIs found)
- Prompt length and Ollama response
- File save operations and paths

