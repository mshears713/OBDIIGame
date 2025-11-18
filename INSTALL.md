# Installation Guide

## Table of Contents

1. [Quick Install](#quick-install)
2. [Detailed Installation](#detailed-installation)
3. [Platform-Specific Instructions](#platform-specific-instructions)
4. [Development Installation](#development-installation)
5. [Troubleshooting](#troubleshooting)
6. [Uninstallation](#uninstallation)

---

## Quick Install

### For Players (Simple Method)

```bash
# Clone the repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### For Players (Package Installation)

```bash
# Install from source
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
pip install .

# Run the game
ecu-rogue
```

---

## Detailed Installation

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package installer)

**Optional:**
- Git (for cloning repository)
- Virtual environment tool (recommended)

### Step 1: Verify Python Installation

```bash
# Check Python version (must be 3.8+)
python --version
# or
python3 --version

# Check pip
pip --version
# or
pip3 --version
```

If Python is not installed:
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** `brew install python3` or download from python.org
- **Linux:** `sudo apt install python3 python3-pip` (Debian/Ubuntu)

### Step 2: Get the Source Code

**Option A: Clone with Git (Recommended)**
```bash
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to a folder
3. Open terminal in that folder

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 4: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# For development (optional)
pip install -r requirements.txt -e .[dev]
```

### Step 5: Verify Installation

```bash
# Run tests to verify
pytest

# Should see: "559 tests passed"
```

### Step 6: Run the Game

```bash
# Standard method
python main.py

# Or if installed as package
ecu-rogue
```

---

## Platform-Specific Instructions

### Windows

#### Installation

```cmd
REM 1. Install Python 3.8+ from python.org
REM    Make sure to check "Add Python to PATH" during installation

REM 2. Open Command Prompt or PowerShell

REM 3. Clone repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

REM 4. Create virtual environment
python -m venv venv

REM 5. Activate virtual environment
venv\Scripts\activate

REM 6. Install dependencies
pip install -r requirements.txt

REM 7. Run game
python main.py
```

#### Terminal Recommendations

For best experience on Windows:
- **Windows Terminal** (recommended) - Download from Microsoft Store
- **PowerShell** - Built-in, good support
- **Command Prompt** - Built-in, basic support

#### Troubleshooting Windows

**Issue:** Python not found
```cmd
REM Add Python to PATH manually
REM Control Panel → System → Advanced → Environment Variables
REM Add: C:\Users\YourName\AppData\Local\Programs\Python\Python3X
```

**Issue:** Permission denied
```cmd
REM Run as Administrator or use:
pip install --user -r requirements.txt
```

### macOS

#### Installation

```bash
# 1. Install Python 3 (if not already installed)
# Using Homebrew (recommended):
brew install python3

# Or download from python.org

# 2. Clone repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Run game
python3 main.py
```

#### Terminal Recommendations

- **Terminal.app** - Built-in, works well
- **iTerm2** - Popular alternative with more features

#### Troubleshooting macOS

**Issue:** Command Line Tools required
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

**Issue:** SSL Certificate errors
```bash
# Update certificates
/Applications/Python\ 3.X/Install\ Certificates.command
```

### Linux

#### Installation

**Debian/Ubuntu:**
```bash
# 1. Install Python 3 and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# 2. Clone repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Run game
python3 main.py
```

**Fedora/RHEL/CentOS:**
```bash
# 1. Install Python 3
sudo dnf install python3 python3-pip git

# 2-6. Same as Debian/Ubuntu above
```

**Arch Linux:**
```bash
# 1. Install Python
sudo pacman -S python python-pip git

# 2-6. Same as above
```

#### Terminal Recommendations

- **GNOME Terminal** - Standard on Ubuntu/Fedora
- **Konsole** - Standard on KDE
- **Alacritty** - Fast, GPU-accelerated

#### Troubleshooting Linux

**Issue:** Permission denied for pip
```bash
# Use --user flag
pip3 install --user -r requirements.txt

# Or use virtual environment (recommended)
```

**Issue:** Module not found after install
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Verify installation
pip3 list
```

---

## Development Installation

For contributors and developers:

### Clone and Install in Development Mode

```bash
# 1. Clone repository
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Install in editable mode with dev dependencies
pip install -e .[dev]

# This installs:
# - pytest (testing)
# - pytest-cov (coverage)
# - mypy (type checking)
# - black (code formatting)
# - flake8 (linting)
```

### Verify Development Setup

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src/

# Code formatting (check)
black --check src/

# Code formatting (apply)
black src/

# Linting
flake8 src/
```

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Now commits will be automatically checked
```

---

## Docker Installation (Alternative)

### Using Docker

```dockerfile
# Dockerfile (create this file)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```bash
# Build image
docker build -t ecu-rogue .

# Run game
docker run -it ecu-rogue
```

---

## Package Installation Methods

### Method 1: Install from Source (Editable)

```bash
# Best for development
pip install -e .

# Run from anywhere
ecu-rogue
```

### Method 2: Install from Source (Normal)

```bash
# Best for players
pip install .

# Run from anywhere
ecu-rogue
```

### Method 3: Install from Wheel

```bash
# Build wheel
python setup.py bdist_wheel

# Install wheel
pip install dist/ecu_rogue-1.0.0-py3-none-any.whl
```

### Method 4: Install from requirements.txt

```bash
# Minimal installation (just dependencies)
pip install -r requirements.txt

# Run from project directory only
python main.py
```

---

## Troubleshooting

### Common Issues

#### Issue: ModuleNotFoundError

**Symptom:**
```
ModuleNotFoundError: No module named 'src'
```

**Solutions:**
```bash
# 1. Make sure you're in the project directory
cd /path/to/OBDIIGame

# 2. Reinstall dependencies
pip install -r requirements.txt

# 3. Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue: pip: command not found

**Symptom:**
```
pip: command not found
```

**Solutions:**
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt

# Install pip
python -m ensurepip --upgrade
```

#### Issue: Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# Or install for user only
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

#### Issue: Wrong Python Version

**Symptom:**
```
Python 3.7 is not supported (need 3.8+)
```

**Solutions:**
```bash
# Check available Python versions
python3 --version
python3.8 --version
python3.9 --version

# Use specific version
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Tests Failing

**Symptom:**
```
pytest: 10 tests failed
```

**Solutions:**
```bash
# 1. Make sure dependencies are installed
pip install -r requirements.txt

# 2. Run from project root
cd /path/to/OBDIIGame
pytest

# 3. Check Python version
python --version  # Should be 3.8+

# 4. Reinstall from scratch
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# 1. Deactivate virtual environment
deactivate

# 2. Remove virtual environment folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Uninstall Package

```bash
# If installed with pip install
pip uninstall ecu-rogue

# If installed with pip install -e
pip uninstall ecu-rogue
```

### Complete Removal

```bash
# 1. Uninstall package
pip uninstall ecu-rogue

# 2. Remove virtual environment
deactivate
rm -rf venv

# 3. Remove project directory
cd ..
rm -rf OBDIIGame
```

---

## Verification Checklist

After installation, verify everything works:

- [ ] Python version is 3.8 or higher
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows pytest)
- [ ] Tests pass (`pytest` shows 559 tests passed)
- [ ] Game runs (`python main.py` or `ecu-rogue`)
- [ ] No error messages

---

## Additional Resources

### Documentation
- **QUICKSTART.md** - Quick guide for players
- **README.md** - Project overview
- **docs/** - Detailed documentation

### Getting Help
- GitHub Issues: Report bugs and ask questions
- Documentation: Check docs/ folder
- Code Comments: Extensive inline documentation

---

## Next Steps

After successful installation:

1. **Read QUICKSTART.md** - Learn how to play
2. **Run tutorial** - `python main.py` then press `[T]`
3. **Explore documentation** - Check `docs/` folder
4. **Join community** - Contribute and share

---

**Installation complete! Enjoy the game!** 🎮
