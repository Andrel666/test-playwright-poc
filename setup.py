#!/usr/bin/env python3
"""
Setup script for AI-Generated Frontend Test Suite
This script helps set up the development environment including virtual environment and dependencies.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_virtual_environment():
    """Check if we're in a virtual environment"""
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    return in_venv

def create_virtual_environment():
    """Create a virtual environment"""
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"📁 Virtual environment '{venv_name}' already exists")
        return True
    
    # Try python3 first, then python
    python_cmd = "python3" if shutil.which("python3") else "python"
    
    if not run_command(f"{python_cmd} -m venv {venv_name}", f"Creating virtual environment '{venv_name}'"):
        return False
    
    print(f"✅ Virtual environment created: {venv_name}")
    return True

def get_activation_command():
    """Get the correct activation command based on OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install Python dependencies"""
    # Use python3 if available, otherwise python
    python_cmd = "python3" if shutil.which("python3") else "python"
    pip_cmd = f"{python_cmd} -m pip install --upgrade pip"
    
    if not run_command(pip_cmd, "Upgrading pip"):
        return False
    
    if not run_command(f"{python_cmd} -m pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    return True

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if os.path.exists(".env"):
        print("📄 .env file already exists")
        return True
    
    if os.path.exists(".env.example"):
        if run_command("cp .env.example .env", "Creating .env file from .env.example", check=False):
            print("✅ .env file created from .env.example")
            print("📝 Please edit .env file with your configuration")
            return True
    
    print("⚠️ No .env.example found, creating complete .env file")
    basic_env = """# Required Configuration Variables
# All variables below are required for the script to work

# Test Configuration
TEST_OUTPUT_DIR=tests
SUPPORTED_EXTENSIONS=.jsx,.tsx,.js,.ts,.vue,.html

# Ollama Configuration
OLLAMA_MODEL=codellama:instruct
OLLAMA_API_URL=http://localhost:11434/api/generate

# Local Development Server
LOCAL_SERVER_URL=http://localhost:3000
MAX_WAIT_SECONDS=30

# Logging Configuration (optional - leave empty to disable file logging)
LOG_DIR=logs

# Optional: GitHub Token (for private repos)
GITHUB_TOKEN=
"""
    
    try:
        with open(".env", "w") as f:
            f.write(basic_env)
        print("✅ Basic .env file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️ Ollama is not installed or not in PATH")
    print("   Install from: https://ollama.com")
    return False

def main():
    print("🚀 AI-Generated Frontend Test Suite Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in a virtual environment
    if check_virtual_environment():
        print("✅ Already running in a virtual environment")
    else:
        print("⚠️ Not in a virtual environment")
        try:
            create_venv = input("Create a virtual environment? (y/n): ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ Running in non-interactive mode. Skipping virtual environment creation.")
            print("To create a virtual environment manually, run:")
            print(f"   python3 -m venv venv")
            print(f"   {get_activation_command()}")
            create_venv = 'n'
        
        if create_venv in ['y', 'yes']:
            if not create_virtual_environment():
                sys.exit(1)
            print(f"\n📝 To activate the virtual environment, run:")
            print(f"   {get_activation_command()}")
            print("\nThen run this setup script again.")
            sys.exit(0)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check Ollama
    check_ollama()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Make sure Ollama is running: ollama run codellama")
    print("2. Edit .env file if needed")
    print("3. Run: python generate_tests_agent.py <GitHub-Repo-URL>")
    print("\nExample:")
    print("   python generate_tests_agent.py https://github.com/user/repo")

if __name__ == "__main__":
    main()
