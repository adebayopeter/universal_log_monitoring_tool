# Contributing to Universal Log Monitoring Tool

Thank you for your interest in contributing! 🎉

## 🤝 How to Contribute

### 🐛 Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include relevant information**:
   - Operating system and version
   - Python version
   - Error messages and stack traces
   - Steps to reproduce

### 💡 Suggesting Features

1. **Check the roadmap** in README.md
2. **Create a feature request** with detailed description
3. **Explain the use case** and benefits
4. **Consider implementation complexity**

### 🛠️ Code Contributions

#### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/your-username/universal-log-monitoring-tool.git
cd universal-log-monitoring-tool

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install pre-commit hooks
pre-commit install
```

#### Making Changes

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** with appropriate tests
3. **Follow coding standards** (see below)
4. **Update documentation** if needed
5. **Test your changes** thoroughly
6. **Commit with clear messages**

#### Pull Request Process

1. **Update the README.md** with details of changes if applicable
2. **Add tests** for new functionality
3. **Ensure all tests pass**: `python -m pytest`
4. **Update version numbers** if applicable
5. **Create pull request** with detailed description

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** standards
- Use **type hints** for function parameters and return values
- **Docstrings** for all classes and functions
- Maximum line length: **88 characters** (Black formatter)

### Example Code Style

```python
def process_log_line(self, line: str, source: str) -> bool:
    """
    Process a single log line and extract relevant information.
    
    Args:
        line: The log line to process
        source: The source file name
        
    Returns:
        True if line was processed successfully, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Failed to process line: {e}")
        return False
```

### Testing Requirements

- **Unit tests** for all new functions
- **Integration tests** for major features
- **Minimum 80% code coverage**
- Use **pytest** for testing framework

### Documentation

- **Clear commit messages**: Use conventional commits format
- **Inline comments** for complex logic
- **Update README** for new features
- **Add examples** for new functionality

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_log_parser.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

```python
import pytest
from log_parser import LogParser

def test_log_parser_initialization():
    """Test that LogParser initializes correctly."""
    parser = LogParser("test_logs")
    assert parser.log_directory.name == "test_logs"
    assert parser.running is False

def test_detect_framework():
    """Test framework detection functionality."""
    parser = LogParser()
    
    # Test Laravel detection
    laravel_log = "[2024-01-01 12:00:00] local.ERROR: Test error"
    assert parser.detect_framework(laravel_log) == "laravel"
    
    # Test Django detection  
    django_log = "[2024-01-01 12:00:00] ERROR django.request: Test error"
    assert parser.detect_framework(django_log) == "django"
```

## 🎯 Areas for Contribution

### High Priority
- [ ] **Docker containerization**
- [ ] **Additional framework support**
- [ ] **Performance optimizations**
- [ ] **Better error handling**
- [ ] **Documentation improvements**

### Medium Priority
- [ ] **Kubernetes deployment examples**
- [ ] **Advanced alerting rules**
- [ ] **Custom dashboard templates**
- [ ] **Log parsing optimizations**
- [ ] **Configuration management**

### Low Priority
- [ ] **UI improvements**
- [ ] **Additional notification channels**
- [ ] **Log rotation features**
- [ ] **Historical data analysis**

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 📋 Commit Message Format

Use conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(parser): add support for Spring Boot log format

Add regex patterns and detection logic for Spring Boot
application logs with timestamp and thread information.

Closes #123
```

```
fix(dashboard): correct payment success rate calculation

The calculation was not accounting for warning-level logs
which should be considered successful payments.

Fixes #456
```

## 🔍 Code Review Process

### For Contributors
- **Be responsive** to feedback
- **Make requested changes** promptly
- **Explain your reasoning** for design decisions
- **Keep PRs focused** and reasonably sized

### For Reviewers
- **Be constructive** and respectful
- **Explain the reasoning** behind suggestions
- **Focus on code quality** and maintainability
- **Test the changes** when possible

## 🎉 Recognition

Contributors are recognized in:
- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub releases** notes

## 📞 Getting Help

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bug reports and feature requests
- **Email**: maintainer@example.com for private matters

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Documentation](https://grafana.com/docs/)

Thank you for contributing to Universal Log Monitoring Tool! 🙏