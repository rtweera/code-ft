# Contributing Guidelines

Thank you for your interest in contributing to code-ft! This document provides guidelines and procedures for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Commit Messages](#commit-messages)
7. [Pull Requests](#pull-requests)
8. [Coding Standards](#coding-standards)
9. [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to:

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Follow project guidelines
- Report inappropriate behavior

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- GitHub account
- Familiarity with Git/GitHub workflow

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/code-ft.git
cd code-ft

# Add upstream remote
git remote add upstream https://github.com/rtweera/code-ft.git
```

### Create a Branch

```bash
# Fetch latest changes
git fetch upstream

# Create feature branch
git checkout -b feature/your-feature-name upstream/main

# Or for bug fixes
git checkout -b fix/bug-description upstream/main

# Or for documentation
git checkout -b docs/documentation-topic upstream/main
```

## Development Setup

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Verify Setup

```bash
# Check Python version
python --version

# Check imports
python -c "import torch; import transformers; print('OK')"

# Run tests
pytest
```

## Making Changes

### Code Organization

Follow the existing directory structure:

```
data-processing/      # Data handling code
training/            # Training scripts
models/              # Model utilities
utils/               # Utility functions
docs/                # Documentation
tests/               # Test files (if added)
```

### File Naming

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_CASE`

### Code Style

Follow PEP 8 guidelines:

```python
# Good
def process_dataset(input_path: str, output_path: str) -> None:
    """Process dataset from input to output."""
    if os.path.exists(input_path):
        data = load_data(input_path)
        formatted = format_data(data)
        save_data(formatted, output_path)

# Bad
def ProcessDataset(inputPath, outputPath):
    data=load_data(inputPath)
    formatted=format_data(data)
    save_data(formatted,outputPath)
```

### Type Hints

Always include type hints:

```python
# Good
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return result."""
    return a + b

# Bad
def add_numbers(a, b):
    return a + b
```

### Docstrings

Use Google-style docstrings:

```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """Brief description of function.
    
    Longer description explaining what the function does,
    how it works, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Dictionary containing results with keys:
        - 'result': The main result
        - 'metadata': Additional information
    
    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is not an integer
    
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result['result'])
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    if not isinstance(param2, int):
        raise TypeError("param2 must be an integer")
    
    # Implementation
    return {"result": "value", "metadata": "info"}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_curator.py

# Run with coverage
pytest --cov=data_processing

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import pytest
from data_processing.curate_dataset import DatasetCurator

class TestDatasetCurator:
    """Test suite for DatasetCurator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.curator = DatasetCurator()
    
    def test_initialization(self):
        """Test curator initialization."""
        assert self.curator is not None
        assert self.curator.random_seed == 42
    
    def test_validate_split_ratios_valid(self):
        """Test validation with valid ratios."""
        self.curator.train_size = 0.8
        self.curator.val_size = 0.1
        self.curator.test_size = 0.1
        
        # Should not raise
        self.curator.validate_split_ratios()
    
    def test_validate_split_ratios_invalid(self):
        """Test validation with invalid ratios."""
        self.curator.train_size = 0.9
        self.curator.val_size = 0.2
        self.curator.test_size = 0.1
        
        with pytest.raises(ValueError):
            self.curator.validate_split_ratios()
```

### Test Coverage Goal

- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Include both positive and negative tests
- Test with realistic data

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance, dependencies, etc.

### Examples

```bash
# Feature
git commit -m "feat(data): add dataset filtering by language"

# Bug fix
git commit -m "fix(trainer): correct learning rate scheduler initialization"

# Documentation
git commit -m "docs: add setup guide for GPU installation"

# Refactoring
git commit -m "refactor(utils): simplify resource monitoring code"
```

## Pull Requests

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Check code style**:
   ```bash
   black .
   flake8 .
   mypy .
   ```

4. **Update documentation** if needed

### PR Title

Use the same format as commits:
```
feat(data): add dataset validation functionality
```

### PR Description

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Related Issues
Closes #123

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] Code follows style guidelines
- [ ] Changes are documented
- [ ] Tests added/updated
- [ ] No new warnings generated
- [ ] Version numbers updated (if applicable)
```

### PR Review Process

1. Automated checks run (tests, linting)
2. Code review by maintainers
3. Requested changes (if any)
4. Approval and merge

## Coding Standards

### Import Organization

```python
# Standard library
import os
import sys
from typing import List, Dict

# Third-party
import torch
import numpy as np
from transformers import AutoTokenizer

# Local
from data_processing.curate_dataset import DatasetCurator
from utils.fine_tuning_profiler import ResourceMonitor
```

### Error Handling

```python
# Good
try:
    result = process_data(data)
except FileNotFoundError as e:
    logger.error(f"Data file not found: {e}")
    raise
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
    raise

# Bad
try:
    result = process_data(data)
except:
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

### Constants

```python
# Good
MAX_SEQUENCE_LENGTH = 512
DEFAULT_BATCH_SIZE = 32
MODEL_CACHE_DIR = "/path/to/cache"

# Bad
max_len = 512
batch_size = 32
cache_dir = "/path/to/cache"
```

## Documentation

### Updating Documentation

When adding features, update relevant documentation:

- **README.md**: Major features or changes
- **ARCHITECTURE.md**: System changes
- **API_REFERENCE.md**: New classes or functions
- **TRAINING.md**: Training modifications
- **Docstrings**: In code comments

### Documentation Format

Use Markdown with:
- Clear headings (# for main, ## for sections)
- Code blocks with language specification
- Examples for complex topics
- Links to related documentation

```markdown
## Feature Name

Description of feature.

### Usage

```python
# Example code
feature.do_something()
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| param1    | str  | None    | Parameter 1 |
| param2    | int  | 10      | Parameter 2 |
```

## Questions?

- Open an issue for questions
- Check existing issues for similar questions
- Review documentation before asking
- Provide context and reproducible examples

## Recognition

Contributors are recognized in:
- Git commit history
- Project changelog
- README acknowledgments (for significant contributions)

---

Thank you for contributing to code-ft! 🙏
