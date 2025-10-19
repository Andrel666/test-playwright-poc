# 🤖 AI-Powered Playwright Test Generator

An advanced, integrated test generation system that uses LLM (Ollama) to automatically generate comprehensive Playwright tests from any frontend codebase. Features enhanced user flow analysis and detailed component understanding for production-ready test generation.

## ✨ Key Features

- 🔍 **Universal Framework Detection**: Automatically detects React, Vue, Angular, or Svelte projects
- 📁 **Comprehensive Code Analysis**: Deep analysis of components, routes, APIs, and UI elements
- 🧠 **Enhanced User Flow Generation**: Detailed user flow analysis with specific UI interactions
- 🎯 **Context-Aware Test Generation**: Uses detailed component analysis for realistic test scenarios
- 📊 **Dependency Graph Analysis**: Builds code dependency graphs for better understanding
- 🔧 **Advanced Prompt Engineering**: Rich, context-aware prompts for superior LLM generation
- 📝 **Comprehensive Logging**: Detailed logs and analysis reports
- 🚀 **Production-Ready Tests**: Generates 4 types of comprehensive test files

## 🏗️ Architecture

The system uses an integrated approach combining:

- **Repository Analysis**: Clone and analyze frontend codebases
- **Component Analysis**: Extract UI elements, forms, buttons, and interactions
- **User Flow Generation**: Generate detailed user flows using LLM analysis
- **Test Generation**: Create comprehensive Playwright tests based on real application behavior

## 📦 Project Structure

```bash
ai-playwright-generator/
├── 📁 tests/                    # Generated test files
│   ├── visual.spec.ts          # Visual regression tests
│   ├── flow.spec.ts            # User journey tests
│   ├── component.spec.ts       # Component interaction tests
│   └── accessibility.spec.ts   # Accessibility compliance tests
├── 📁 reports/                  # Analysis reports
│   ├── user_flows.md           # User flow descriptions
│   └── analysis_report_*.md    # Comprehensive analysis reports
├── 📁 logs/                     # Execution logs
│   └── *.log                   # Detailed execution logs
├── 📄 integrated_test_generator.py  # Main integrated system
├── 📄 setup.py                 # Environment setup script
├── 📄 requirements.txt         # Python dependencies
└── 📄 readme.md               # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+**
- **Ollama** with a code model (e.g., `codellama:instruct`, `deepseek-coder:6.7b`)
- **Node.js 16+** (for Playwright)

### 2. Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-playwright-generator

# Run automated setup
python3 setup.py
```

This will:
- ✅ Check Python version compatibility
- 🐍 Create a virtual environment
- 📦 Install all dependencies
- ⚙️ Create `.env` file from template
- 🦙 Check Ollama installation

### 3. Configure Environment

Edit `.env` file with your settings:

```env
# Ollama Configuration
OLLAMA_MODEL=codellama:instruct
OLLAMA_API_URL=http://localhost:11434/api/generate

# Test Configuration
TEST_OUTPUT_DIR=tests
LOG_DIR=logs
REPORT_DIR=reports

# Local Development Server
LOCAL_SERVER_URL=http://localhost:3000
MAX_WAIT_SECONDS=30

# Optional: GitHub Token (for private repos)
GITHUB_TOKEN=
```

### 4. Start Ollama

```bash
# Install and run a code model
ollama run codellama:instruct
# or
ollama run deepseek-coder:6.7b
```

### 5. Generate Tests

```bash
python3 integrated_test_generator.py https://github.com/example/frontend-app
```

## 🧠 How It Works

### **Step 1: Repository Analysis** 📥
- Clones the target repository
- Detects frontend framework (React, Vue, Angular, Svelte)
- Collects all source files (`.tsx`, `.jsx`, `.vue`, `.html`, etc.)
- Builds dependency graph of components

### **Step 2: Enhanced Component Analysis** 🔍
- Analyzes component files for UI elements
- Extracts form fields, buttons, validation rules
- Identifies API calls and state management
- Maps user interactions and component behavior

### **Step 3: User Flow Generation** 📋
- Uses LLM to generate detailed user flows
- Includes specific UI elements and interactions
- Covers validation, error handling, and edge cases
- Creates actionable flow descriptions for test generation

### **Step 4: Test Generation** 🧠
- Generates 4 comprehensive test files using enhanced prompts
- Uses detailed user flows as context
- Creates realistic test scenarios based on actual application behavior
- Includes API mocking and error handling

### **Step 5: Analysis & Reports** 📊
- Generates comprehensive analysis reports
- Saves user flow descriptions
- Provides detailed execution logs
- Creates Graphviz dependency graphs

## 🧪 Generated Test Types

### **Visual Tests** (`visual.spec.ts`)
- Responsive design testing across viewport sizes
- Dark/light theme switching
- Loading states and animations
- Error states and empty states
- Visual regression testing with screenshots

### **Flow Tests** (`flow.spec.ts`)
- Complete user journeys based on generated user flows
- Form submission with validation
- Navigation between pages
- User authentication flows
- Error handling and recovery
- API integration with proper mocking

### **Component Tests** (`component.spec.ts`)
- Interactive element testing (buttons, forms, modals)
- Component state changes and updates
- Keyboard navigation and accessibility
- Component-specific functionality
- Edge cases and error scenarios

### **Accessibility Tests** (`accessibility.spec.ts`)
- ARIA labels and roles compliance
- Keyboard navigation and focus management
- Screen reader compatibility
- Color contrast and visual accessibility
- Focus management and tab order

## 📊 Enhanced Features

### **Detailed User Flow Analysis**
The system generates comprehensive user flows that include:
- Specific UI elements (button text, input placeholders)
- Detailed interaction sequences
- Validation rules and error handling
- State management and API integration
- Edge cases and error scenarios

### **Component Analysis**
- **Form Elements**: Extracts input fields, validation rules, submit handlers
- **UI Elements**: Categorizes buttons, modals, navigation, dropdowns
- **API Integration**: Identifies API calls and request/response patterns
- **State Management**: Analyzes component state and data flow

### **Context-Aware Test Generation**
- Uses actual component analysis for realistic test scenarios
- Generates tests based on real application behavior
- Includes specific selectors and interactions
- Covers validation, error handling, and edge cases

## 🔧 Advanced Configuration

### **Analysis Configuration**
```env
# File Analysis
MAX_FILE_SIZE=10000          # Maximum file size to analyze
MAX_WAIT_SECONDS=30          # Maximum wait time for app startup

# Feature Flags
ENABLE_USER_FLOW_GENERATION=true
ENABLE_COMPONENT_ANALYSIS=true
ENABLE_DEPENDENCY_GRAPH=true
```

### **LLM Configuration**
```env
# Ollama Settings
OLLAMA_MODEL=codellama:instruct
OLLAMA_API_URL=http://localhost:11434/api/generate

# Alternative models
# OLLAMA_MODEL=deepseek-coder:6.7b
# OLLAMA_MODEL=llama3.1:8b
```

## 📈 Expected Results

### **Test Quality Improvements**
- **Realistic Selectors**: Uses actual component selectors and interactions
- **Comprehensive Coverage**: Covers all major user flows and components
- **Edge Case Testing**: Includes error scenarios and validation testing
- **API Integration**: Proper API mocking and error handling
- **Accessibility**: Full accessibility compliance testing

### **Generated Test Examples**

```typescript
// Enhanced Flow Test Example
test('should complete user login with validation', async ({ page }) => {
  // Mock API response
  await page.route('**/api/auth/login', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ 
      success: true, 
      user: { id: '123', email: 'test@example.com' },
      token: 'mock-jwt-token'
    })
  }));
  
  await page.goto('/login');
  
  // Fill login form with specific selectors
  await page.fill('input[placeholder="Enter your email"]', 'test@example.com');
  await page.fill('input[placeholder="Enter your password"]', 'password123');
  
  // Submit form
  await page.click('button:has-text("Sign In")');
  
  // Verify success
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  await expect(page).toHaveURL('/dashboard');
});

// Component Test Example
test('should handle form validation errors', async ({ page }) => {
  await page.goto('/register');
  
  // Try to submit empty form
  await page.click('button:has-text("Register")');
  
  // Verify validation messages
  await expect(page.locator('text=Please enter your email')).toBeVisible();
  await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible();
});
```

## 🛡️ Limitations

- **Backend Mocking**: API requests are mocked - no real backend integration
- **Model Dependency**: Test quality depends on your local Ollama model capabilities
- **Public Repos**: Currently works with public GitHub repositories only
- **Frontend Focus**: Optimized for frontend-only or frontend-heavy projects

## 🔧 Troubleshooting

### **No Test Files Generated**
- Check the `logs/` directory for detailed debugging info
- Ensure Ollama is running: `ollama run codellama:instruct`
- Verify the repository has frontend source files

### **Framework Not Detected**
- The system recursively searches for `package.json` files
- Check logs to see which package.json files were found
- Ensure the project has frontend dependencies

### **User Flows Too Simple**
- The system now includes enhanced component analysis
- Check `reports/user_flows.md` for detailed flow descriptions
- Ensure components have sufficient UI elements for analysis

### **App Won't Start**
- Check available scripts in the logs
- Manually start the app and run tests: `npx playwright test`
- Verify the app runs on the configured port (default: 3000)

## 📌 Roadmap

- 🚀 **CI Integration**: GitHub Action for automated test generation
- ⚙️ **Configuration UI**: Web interface for test configuration
- 🔄 **Multi-page Crawling**: Automatic discovery of all app routes
- 📊 **Coverage Reports**: Generate comprehensive test coverage analysis
- 🔐 **Private Repos**: Support for private GitHub repositories
- 🎨 **Custom Templates**: User-defined test templates
- 📱 **Mobile Testing**: Support for React Native and mobile frameworks

## 🧑‍💻 Author

Built with ♥️ for the testing community. This integrated system combines the best of automated analysis, LLM-powered generation, and comprehensive test coverage.

---

**For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/example/ai-playwright-generator).**