# Contributing to MedicalCycle Cloud

Thank you for your interest in contributing to MedicalCycle Cloud! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our Code of Conduct.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (recommended)
- Git

### Development Setup

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/medicalCycle-cloud.git
cd medicalCycle-cloud
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Set up development environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

pip install -r requirements-dev.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your local settings
```

5. **Start services with Docker**
```bash
docker-compose up -d postgres redis
```

6. **Run development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Development Workflow

### Before You Start

1. Check existing issues and pull requests
2. Create an issue for your feature/bug fix
3. Wait for feedback before starting work

### While You Work

1. **Write tests first** (TDD approach)
2. **Follow code style** (see below)
3. **Keep commits atomic** and well-documented
4. **Update documentation** as needed
5. **Run tests frequently**

### Code Style

#### Python

- **Formatter**: Black (line length: 100)
- **Linter**: Flake8
- **Type Checker**: MyPy
- **Import Sorter**: isort

```bash
# Format code
black app tests

# Check linting
flake8 app tests

# Type checking
mypy app

# Sort imports
isort app tests
```

#### Naming Conventions

- **Classes**: PascalCase (e.g., `UserModel`)
- **Functions/Methods**: snake_case (e.g., `get_user_by_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)
- **Private**: Leading underscore (e.g., `_internal_method`)

#### Documentation

- **Docstrings**: Google style
- **Comments**: Explain WHY, not WHAT
- **Type hints**: Required for all functions

Example:
```python
def create_user(user_data: UserCreate, db: Session) -> User:
    """
    Create a new user in the database.
    
    Args:
        user_data: User creation data
        db: Database session
        
    Returns:
        Created user object
        
    Raises:
        ValueError: If email already exists
    """
    # Check for existing user
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise ValueError("Email already registered")
    
    # Create and save user
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

## Testing

### Writing Tests

- **Location**: `tests/` directory
- **Naming**: `test_*.py` files
- **Coverage**: Aim for >80% coverage
- **Fixtures**: Use `conftest.py` for shared fixtures

Example test:
```python
def test_create_user(client, db):
    """Test user creation"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "securepass123",
            "role": "patient"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(auth): add JWT token refresh endpoint

Implement refresh token mechanism to extend session without re-authentication.
Tokens expire after 7 days and can be refreshed up to 30 days.

Closes #123
```

```
fix(patients): prevent duplicate patient records

Add unique constraint on user_id in patients table to prevent
multiple patient records for the same user.

Fixes #456
```

## Pull Request Process

1. **Update your branch**
```bash
git fetch origin
git rebase origin/main
```

2. **Push your changes**
```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request**
   - Use descriptive title
   - Reference related issues
   - Describe changes and rationale
   - Include testing instructions

4. **PR Checklist**
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   - [ ] Commit messages are clear

5. **Code Review**
   - Address reviewer feedback
   - Re-request review after changes
   - Minimum 2 approvals required

6. **Merge**
   - Squash commits if requested
   - Delete feature branch after merge

## Documentation

### Updating Documentation

- Update relevant `.md` files in `docs/`
- Update `README.md` for user-facing changes
- Update docstrings for code changes
- Include examples where helpful

### Documentation Standards

- Clear and concise language
- Code examples with syntax highlighting
- Table of contents for long documents
- Links to related documentation

## Reporting Bugs

### Bug Report Template

```markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python: [e.g., 3.11.0]
- FastAPI: [e.g., 0.104.1]

## Additional Context
Any additional information
```

## Feature Requests

### Feature Request Template

```markdown
## Description
Clear description of the feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches considered

## Additional Context
Any additional information
```

## Security

### Reporting Security Issues

**Do not** open public issues for security vulnerabilities.

Please email: security@medicalcycle.local

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Areas for Contribution

### High Priority

- [ ] Frontend (React) implementation
- [ ] Advanced encryption features
- [ ] Multi-factor authentication
- [ ] API rate limiting
- [ ] Advanced search and filtering

### Medium Priority

- [ ] Notification system
- [ ] Reporting and analytics
- [ ] Data export functionality
- [ ] Mobile app API
- [ ] GraphQL API

### Low Priority

- [ ] UI/UX improvements
- [ ] Documentation enhancements
- [ ] Performance optimizations
- [ ] Additional test coverage

## Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Email**: contact@medicalcycle.local

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md
- CONTRIBUTORS.md (future)
- Release notes

Thank you for contributing to MedicalCycle Cloud! 🎉
