# 🤝 Contributing to Try-Harder-AI

Thank you for your interest in contributing to Try-Harder-AI! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Testing Guidelines](#testing-guidelines)
9. [Documentation](#documentation)
10. [Issue Guidelines](#issue-guidelines)
11. [Feature Requests](#feature-requests)
12. [Bug Reports](#bug-reports)
13. [Community](#community)

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race or ethnicity
- Age
- Religion
- Nationality

### Our Standards

**Positive behaviors include:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community
- ✅ Showing empathy towards others

**Unacceptable behaviors include:**
- ❌ Harassment or discriminatory comments
- ❌ Trolling or insulting remarks
- ❌ Personal or political attacks
- ❌ Publishing others' private information
- ❌ Other conduct deemed inappropriate

### Enforcement

Violations of the code of conduct may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: [your-email@example.com]

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.10 or higher** installed
- **Git** for version control
- **Discord account** for testing
- **Google Gemini API key** (for AI features — free at https://aistudio.google.com/apikey)
- Basic knowledge of:
  - Python async programming
  - Discord.py library (slash commands / `app_commands`)
  - YAML/JSON data formats
  - Git workflow

### Project Structure Overview

```
try-harder-ai-complete/
├── bot/              # Core bot code
├── data/             # Data files (YAML/JSON)
├── prompts/          # AI system prompts
├── config/           # Configuration files
├── utils/            # Utility functions
├── tests/            # Unit tests
└── docs/             # Documentation
```

### First Time Contributors

**Great first issues for beginners:**
- 🟢 Documentation improvements
- 🟢 Adding new practice machine recommendations
- 🟢 Expanding certification data
- 🟢 Creating new assessment questions
- 🟢 Fixing typos or formatting

Look for issues tagged with:
- `good first issue`
- `documentation`
- `help wanted`
- `beginner-friendly`

---

## 💡 How to Contribute

### Types of Contributions

1. **Code Contributions**
   - Bug fixes
   - New features
   - Performance improvements
   - Refactoring

2. **Content Contributions**
   - Certification data updates
   - Assessment questions
   - Resource links
   - Practice machine recommendations

3. **Documentation**
   - README improvements
   - Code comments
   - Tutorial creation
   - API documentation

4. **Testing**
   - Writing unit tests
   - Manual testing
   - Bug reporting
   - Edge case identification

5. **Design**
   - UI/UX improvements
   - Discord embed designs
   - Response formatting

---

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/try-harder-ai.git
cd try-harder-ai

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/try-harder-ai.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

**requirements-dev.txt:**
```
# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
pylint>=2.17.0
mypy>=1.4.0

# Documentation
sphinx>=7.0.0
sphinx-rtd-theme>=1.3.0
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**.env contents:**
```bash
# Discord
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_AI_MODEL=gemini-1.5-flash

# Optional
APP_NAME=Try-Harder-AI-Dev
```

### 5. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## 📝 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# ✅ GOOD - Clear, documented code

async def generate_roadmap(
    certification: str,
    skill_level: str,
    duration_weeks: int,
    weak_areas: list[str]
) -> dict:
    """
    Generate personalized study roadmap.
    
    Args:
        certification: Certification code (e.g., 'OSCP')
        skill_level: User's skill level (beginner/intermediate/advanced)
        duration_weeks: Roadmap duration in weeks (6-24)
        weak_areas: List of topics needing focus
        
    Returns:
        Dictionary containing roadmap structure
        
    Raises:
        ValueError: If parameters are invalid
        
    Example:
        >>> roadmap = await generate_roadmap('OSCP', 'intermediate', 12, ['AD'])
        >>> print(roadmap['weeks'][0]['title'])
        'Active Directory Fundamentals'
    """
    # Validate inputs
    if duration_weeks < 6 or duration_weeks > 24:
        raise ValueError("Duration must be between 6 and 24 weeks")
    
    # Load certification data
    cert_data = await load_certification_data(certification)
    
    # Generate roadmap using Gemini AI
    roadmap = await ai_engine.generate_roadmap(
        cert_data,
        skill_level,
        duration_weeks,
        weak_areas
    )
    
    return roadmap


# ❌ BAD - No documentation, unclear names

async def gen(c, s, d, w):
    if d < 6 or d > 24:
        raise ValueError("Invalid")
    data = await load(c)
    r = await ai.gen(data, s, d, w)
    return r
```

### Code Formatting

```bash
# Auto-format with Black
black bot/ tests/ utils/

# Check linting
flake8 bot/ tests/ utils/

# Type checking
mypy bot/
```

### Naming Conventions

```python
# Variables and functions: snake_case
user_data = get_user_data(user_id)
assessment_result = calculate_score(responses)

# Classes: PascalCase
class AssessmentManager:
    pass

class GeminiAI:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_QUESTIONS = 10
DEFAULT_AI_MODEL = "gemini-1.5-flash"
API_TIMEOUT = 60

# Private methods: _leading_underscore
def _internal_helper():
    pass

async def _make_api_request():
    pass
```

### Async/Await Guidelines

```python
# ✅ GOOD - Proper async usage with slash commands

async def process_slash_command(interaction: discord.Interaction, user_input: str):
    """Process slash command interaction asynchronously"""
    await interaction.response.defer()  # Required — prevents interaction timeout
    try:
        # Async operations
        user_data = await load_user_data(interaction.user.id)
        response = await ai_engine.generate(user_input)
        await save_user_data(interaction.user.id, user_data)

        # Send followup response
        await interaction.followup.send(response)

    except Exception as e:
        logger.error(f"Slash command error: {e}")
        await interaction.followup.send("❌ An error occurred. Please try again.")


# ❌ BAD - Blocking operations in async function

async def process_slash_command(interaction: discord.Interaction, user_input: str):
    user_data = load_user_data_sync(interaction.user.id)  # Blocking!
    time.sleep(2)                                          # Blocking!
    response = requests.post(api_url, data=user_input)    # Blocking!
```

### Error Handling

```python
# ✅ GOOD - Specific exception handling

async def fetch_user_data(user_id: str) -> dict:
    """Fetch user data with proper error handling"""
    try:
        with open(f"data/users/{user_id}.json", "r") as f:
            data = json.load(f)
        return data
        
    except FileNotFoundError:
        logger.warning(f"User {user_id} not found, creating new profile")
        return create_new_user(user_id)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON for user {user_id}: {e}")
        raise ValueError(f"Corrupted user data for {user_id}")
        
    except Exception as e:
        logger.exception(f"Unexpected error loading user {user_id}")
        raise


# ❌ BAD - Bare except

async def fetch_user_data(user_id: str) -> dict:
    try:
        with open(f"data/users/{user_id}.json", "r") as f:
            return json.load(f)
    except:  # Too broad!
        return {}  # Silent failure!
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD - Appropriate log levels

logger.debug(f"Processing slash command: {command_name}")   # Detailed info
logger.info(f"User {user_id} started assessment")           # General info
logger.warning(f"Rate limit approaching for {user_id}")     # Warnings
logger.error(f"Gemini API request failed: {error}")         # Errors
logger.critical(f"Database connection lost!")               # Critical issues

# Include context in logs
logger.info(
    "Assessment completed",
    extra={
        "user_id": user_id,
        "certification": cert,
        "score": score,
        "duration_seconds": duration
    }
)
```

### Type Hints

```python
from typing import Optional, List, Dict, Union, Any

# ✅ GOOD - Type hints for clarity

async def calculate_score(
    responses: List[str],
    correct_answers: List[str],
    difficulty_levels: List[str]
) -> Dict[str, Union[int, float, bool]]:
    """Calculate assessment score with type hints"""
    total_points: int = 0
    max_points: int = 30
    
    # Implementation...
    
    return {
        "total_points": total_points,
        "max_points": max_points,
        "percentage": (total_points / max_points) * 100,
        "passed": total_points >= 21
    }
```

---

## 📋 Commit Guidelines

### Commit Message Format

We follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
feat(assessment): add advanced difficulty questions for OSEP
feat(roadmap): implement milestone tracking system

# Bug fix
fix(ai_engine): resolve timeout error on long Gemini prompts
fix(commands): correct permission check for admin slash commands

# Documentation
docs(readme): update installation instructions
docs(api): add Gemini API integration examples

# Refactoring
refactor(user_manager): simplify data loading logic
refactor(commands): extract common slash command validation functions

# Testing
test(assessment): add unit tests for score calculation
test(ai_engine): add mock Gemini API response tests

# Chore
chore(deps): update discord.py to v2.3.2
chore(deps): update google-generativeai to latest version
chore(ci): add GitHub Actions workflow
```

### Writing Good Commit Messages

**✅ GOOD:**
```bash
feat(oscp): add 10 new buffer overflow questions

- Added questions covering stack-based overflows
- Included EIP control scenarios
- Added shellcode development questions
- Updated difficulty ratings

Closes #42
```

**❌ BAD:**
```bash
update stuff
fixed bug
wip
asdfgh
```

### Commit Best Practices

1. **One logical change per commit**
   ```bash
   # ✅ Good - Separate commits
   git commit -m "feat(data): add KLCP certification data"
   git commit -m "docs(klcp): add KLCP documentation"
   
   # ❌ Bad - Mixed changes
   git commit -m "add klcp and fix typos and update readme"
   ```

2. **Meaningful commit messages**
3. **Reference issues when applicable**
4. **Keep commits atomic and reversible**

---

## 🔄 Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main branch
- [ ] Commit messages follow guidelines
- [ ] PR description is clear and complete

### Creating a Pull Request

1. **Update your fork**
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Rebase your feature branch**
   ```bash
   git checkout feature/your-feature
   git rebase main
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```

4. **Create PR on GitHub**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Related Issues
Closes #123
Related to #456

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally

## Additional Notes
Any additional information reviewers should know.
```

### Review Process

1. **Automated Checks**
   - Linting (flake8)
   - Type checking (mypy)
   - Tests (pytest)
   - Code coverage

2. **Manual Review**
   - Code quality
   - Logic correctness
   - Performance implications
   - Security considerations

3. **Feedback & Iteration**
   - Address reviewer comments
   - Make requested changes
   - Push updates to same branch

4. **Approval & Merge**
   - At least 1 approval required
   - All checks must pass
   - Squash and merge (default)

---

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bot --cov-report=html

# Run specific test file
pytest tests/test_assessment.py

# Run specific test
pytest tests/test_assessment.py::test_score_calculation

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

### Writing Tests

```python
# tests/test_assessment.py

import pytest
from bot.assessment import AssessmentManager

@pytest.fixture
def assessment_manager():
    """Fixture providing AssessmentManager instance"""
    return AssessmentManager()

@pytest.fixture
def sample_questions():
    """Fixture providing sample questions"""
    return [
        {
            "id": "test_001",
            "question": "What is OSCP?",
            "options": {"A": "Option 1", "B": "Option 2"},
            "correct_answer": "A",
            "difficulty": "beginner"
        }
    ]

class TestAssessmentManager:
    """Test suite for AssessmentManager"""
    
    def test_score_calculation(self, assessment_manager):
        """Test score calculation logic"""
        responses = ["A", "B", "C"]
        correct = ["A", "B", "C"]
        difficulties = ["beginner", "intermediate", "advanced"]
        
        result = assessment_manager.calculate_score(
            responses, 
            correct, 
            difficulties
        )
        
        assert result["total_points"] == 6  # 1+2+3
        assert result["percentage"] == 100
        assert result["passed"] is True
    
    @pytest.mark.asyncio
    async def test_load_questions(self, assessment_manager):
        """Test question loading from YAML"""
        questions = await assessment_manager.load_questions("OSCP")
        
        assert len(questions) > 0
        assert "beginner" in questions
        assert "intermediate" in questions
        assert "advanced" in questions
    
    def test_invalid_certification(self, assessment_manager):
        """Test handling of invalid certification"""
        with pytest.raises(ValueError):
            assessment_manager.load_questions("INVALID_CERT")


# tests/test_ai_engine.py

import pytest
from unittest.mock import MagicMock, patch
from bot.ai_engine import GeminiAI

@pytest.fixture
def gemini_ai():
    """Fixture providing GeminiAI instance with mocked API key"""
    with patch.dict("os.environ", {"GEMINI_API_KEY": "AIzaSy_test_key"}):
        return GeminiAI()

class TestGeminiAI:
    """Test suite for GeminiAI engine"""

    @pytest.mark.asyncio
    async def test_generate_returns_text(self, gemini_ai):
        """Test that generate() returns a non-empty string"""
        mock_response = MagicMock()
        mock_response.text = "Here is your answer."

        with patch("google.generativeai.GenerativeModel.generate_content",
                   return_value=mock_response):
            result = await gemini_ai.generate("What is OSCP?")

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_missing_api_key_raises(self):
        """Test that missing GEMINI_API_KEY raises ValueError"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                GeminiAI()
```

### Test Coverage Requirements

- **Minimum coverage:** 70%
- **Target coverage:** 85%+
- **Critical modules:** 90%+

---

## 📚 Documentation

### Code Documentation

```python
def complex_function(param1: str, param2: int) -> dict:
    """
    One-line summary of function.
    
    Detailed description of what the function does,
    including any important implementation details.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Dictionary containing:
            - key1: Description
            - key2: Description
            
    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["key1"])
        'value1'
        
    Note:
        Any important notes or warnings.
    """
    pass
```

### Updating Documentation

When changing code, update:
- **Inline comments** for complex logic
- **Docstrings** for functions/classes
- **README.md** for user-facing changes
- **API_INTEGRATION.md** for Gemini API changes
- **ARCHITECTURE.md** for structural changes

---

## 🐛 Issue Guidelines

### Creating Issues

**Good issue template:**

```markdown
**Issue Type:** Bug / Feature Request / Question

**Description:**
Clear and concise description of the issue.

**Steps to Reproduce:** (for bugs)
1. Run slash command `/assess`
2. Select OSCP
3. Answer first question
4. Bot crashes

**Expected Behavior:**
What should happen.

**Actual Behavior:**
What actually happens.

**Environment:**
- OS: Ubuntu 22.04
- Python Version: 3.10.8
- Bot Version: 3.0.0

**Logs/Screenshots:**
```
Error traceback or screenshots
```

**Possible Solution:** (optional)
Suggestions for fixing the issue.
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `duplicate`: Duplicate of existing issue
- `wontfix`: Will not be worked on

---

## 💡 Feature Requests

### Proposing New Features

1. **Search existing issues** to avoid duplicates
2. **Create detailed proposal** with:
   - Use case and benefits
   - Proposed implementation
   - Potential challenges
   - Alternative solutions considered

3. **Discuss before implementing**
   - Open issue for discussion
   - Wait for feedback/approval
   - Refine based on comments

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature.

## Problem It Solves
What problem does this solve for users?

## Proposed Solution
How should this feature work?

## Implementation Ideas
Technical approach suggestions.

## Alternatives Considered
What other approaches were considered?

## Additional Context
Screenshots, examples, references, etc.
```

---

## 🤔 Questions & Support

### Getting Help

- **Documentation:** Check docs/ folder first
- **Issues:** Search existing GitHub issues
- **Discord:** Join our community Discord
- **Email:** contact@try-harder-ai.com

### Asking Good Questions

**✅ Good question:**
```
I'm trying to add a new certification but getting a KeyError when 
loading questions. I've added the cert to certifications.yaml and 
created questions in questions.yaml. Here's my code:

[code snippet]

And here's the error:
[error message]

I think it might be related to YAML structure, but I'm not sure.
```

**❌ Bad question:**
```
help it doesn't work
```

---

## 🎯 Contribution Ideas

### Easy Contributions

- Add new practice machine recommendations
- Expand certification descriptions
- Create more assessment questions
- Fix typos and grammar
- Improve code comments
- Update outdated links

### Medium Contributions

- Add new certification support
- Implement additional Gemini model variants
- Create utility functions
- Improve error messages
- Optimize performance
- Add logging enhancements

### Advanced Contributions

- Database migration (JSON → PostgreSQL)
- Web dashboard development
- Advanced caching system
- Multi-server support
- Analytics implementation
- CI/CD pipeline improvements
- Gemini multimodal support (image/PDF analysis)

---

## 🌟 Recognition

### Contributors

All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

### Top Contributors

Special recognition for:
- Most commits
- Most impactful features
- Best documentation
- Outstanding reviews
- Community support

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, makes Try-Harder-AI better!

**Ways to contribute:**
- 💻 Code
- 📝 Documentation
- 🐛 Bug reports
- 💡 Feature ideas
- ⭐ Star the project
- 🗣️ Spread the word

---

## 📞 Contact

- **GitHub Issues:** https://github.com/The4v1/Try-Harder-AI/issues
- **Discord:** https://discord.gg/try-harder-ai
- **Email:** contribute@try-harder-ai.com
- **Twitter:** @TryHarderAI

---

*Last Updated: February 2026*
*Version: 3.0.0*
*Happy Contributing! 🚀*