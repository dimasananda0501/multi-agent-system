# Contributing to XYZ AI Nexus

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Follow project standards

## How to Contribute

### Reporting Bugs

**Before submitting:**
- Check existing issues
- Verify it's actually a bug (not expected behavior)
- Test with latest version

**When submitting:**
1. Use GitHub Issues
2. Clear title (e.g., "Agent fails with timeout on long queries")
3. Include:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (Python version, OS, etc.)
   - Relevant logs/errors

**Template:**
```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.11.5
- OS: Ubuntu 22.04
- API: OpenAI GPT-4o

## Logs/Screenshots
```

### Suggesting Features

**Good feature requests include:**
- Clear use case
- Expected behavior
- Why it's valuable
- Potential implementation approach (optional)

**Open a discussion first** before spending time on implementation.

### Pull Requests

**Before starting:**
1. Open an issue or discussion
2. Get feedback on approach
3. Fork the repository

**Development process:**

1. **Create branch:**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

2. **Make changes:**
   - Follow code style (Black + Ruff)
   - Add tests for new features
   - Update documentation
   - Add docstrings to new functions

3. **Test locally:**
```bash
# Run tests
pytest

# Check formatting
black .
ruff check .

# Test manually
python main.py
python examples/demo.py
```

4. **Commit:**
```bash
git add .
git commit -m "Add: Clear description of changes"
# Use prefixes: Add, Fix, Update, Remove, Refactor
```

5. **Push and create PR:**
```bash
git push origin feature/your-feature-name
# Then create Pull Request on GitHub
```

**PR Guidelines:**
- Clear title and description
- Link related issues
- Include tests
- Update documentation
- Keep changes focused (one feature/fix per PR)
- Respond to review feedback

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- Virtual environment tool (venv/conda)

### Setup Steps

```bash
# 1. Fork and clone
git clone https://github.com/dimasananda0501/multi-agent-system.git
cd xyz-ai-nexus

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# 5. Configure environment
cp .env.example .env
# Add your API keys to .env

# 6. Run tests to verify setup
pytest
```

## Code Style

### Python Style Guide

**We use:**
- **Black** for formatting
- **Ruff** for linting
- **Type hints** where helpful
- **Docstrings** for all public functions

**Example:**
```python
def process_query(query: str, user_id: str) -> Dict[str, Any]:
    """
    Process user query through multi-agent system.
    
    Args:
        query: User's natural language question
        user_id: Unique identifier for the user
    
    Returns:
        Dictionary containing response and metadata
    
    Example:
        >>> process_query("What is production?", "user_123")
        {"response": "...", "agents": ["upstream"]}
    """
    # Implementation
    pass
```

### Commit Messages

**Format:**
```
Type: Short description (max 50 chars)

Longer explanation if needed (wrap at 72 chars).
Explain WHY the change was made, not just what.

- Bullet points for details
- Reference issues: Fixes #123
```

**Types:**
- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Modify existing feature
- `Remove`: Delete feature/code
- `Refactor`: Code restructuring
- `Docs`: Documentation changes
- `Test`: Add/modify tests
- `Style`: Code style changes

**Examples:**
```
Add: Implement Finance Agent with cost analysis tools

Fix: Resolve timeout issue in multi-agent queries (#42)

Update: Improve orchestrator routing accuracy

Docs: Add deployment guide for Hugging Face Spaces
```

## Testing

### Writing Tests

**Test file structure:**
```python
# tests/test_feature.py

import pytest
from src.module import function

class TestFeatureName:
    """Test suite for specific feature"""
    
    def test_happy_path(self):
        """Test normal usage"""
        result = function("input")
        assert result == expected
    
    def test_edge_case(self):
        """Test boundary conditions"""
        # Test implementation
    
    def test_error_handling(self):
        """Test error scenarios"""
        with pytest.raises(ValueError):
            function("invalid")
```

**Run tests:**
```bash
# All tests
pytest

# Specific file
pytest tests/test_agents.py

# With coverage
pytest --cov=src

# Verbose
pytest -v

# Skip slow tests
pytest -m "not slow"
```

### Test Coverage

Aim for >80% coverage for new code. Check with:
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def calculate_revenue(volume: int, price: float) -> float:
    """
    Calculate total revenue from oil volume and price.
    
    Args:
        volume: Oil volume in barrels
        price: Price per barrel in USD
    
    Returns:
        Total revenue in USD
    
    Raises:
        ValueError: If volume or price is negative
    
    Example:
        >>> calculate_revenue(1000, 85.0)
        85000.0
    """
```

### README Updates

When adding features, update:
- [ ] Main README.md
- [ ] Architecture docs if structure changes
- [ ] API docs if endpoints change
- [ ] Deployment docs if setup changes

## Project Structure

```
xyz-ai-nexus/
├── src/                    # Source code
│   ├── agents/            # Agent implementations
│   ├── orchestrator/      # Orchestration logic
│   ├── tools/             # Agent tools
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Usage examples
└── deployment/            # Deployment configs
```

**Adding new agent:**
1. Create agent file in `src/agents/`
2. Create tools in `src/tools/`
3. Register in orchestrator
4. Add tests
5. Update documentation

## Review Process

**What reviewers look for:**
- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations
- Breaking changes

**Timeline:**
- Initial review: 2-3 days
- Follow-up: 1-2 days
- Maintainers are volunteers - be patient!

## Getting Help

**Stuck? Ask for help!**
- **Discussions:** General questions
- **Issues:** Bug-specific help
- **Discord:** Real-time chat (coming soon)

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors graph

Thank you for contributing! 🙏

---

**Questions?** Open a discussion or contact maintainers.
