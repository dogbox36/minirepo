# Mini Pytest API Tests

Production-quality, configuration-driven API testing framework example using Pytest, Requests, and Pydantic.
Targeting [Requirements.in](https://reqres.in/) as a demo API.

## Features
- **Configurable**: Environment-based configuration (dev, staging) via YAML and ENV vars.
- **Robust Client**: Wrapper around `requests` with automatic logging and retry logic.
- **Validation**: Strict response schema validation using `Pydantic`.
- **Reporting**: HTML test reports generated automatically.
- **CI/CD**: GitHub Actions workflow included.
- **Code Quality**: Pre-configured `ruff`, `black`, and `mypy`.

## Project Structure
```text
mini-pytest-api-tests/
├── config/                 # Environment specific configurations
├── src/
│   └── apitest/           # Core framework logic (client, config, schemas)
├── tests/                  # Test suites
│   ├── conftest.py        # Fixtures (client, session)
│   ├── test_users.py      # Feature tests
│   └── test_other.py      # Parametrized examples
├── .github/workflows/      # CI Pipeline
├── Makefile                # Shortcut commands
└── pyproject.toml          # Dependencies & Tool config
```

## Quickstart

### Prerequisites
- Python 3.9+

### Installation
1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd mini-pytest-api-tests
   ```
2. Install dependencies:
   ```bash
   # Using Makefile (Linux/Mac/WSL)
   make install
   
   # Or manually
   pip install -e .[dev]
   ```

### Running Tests
By default, tests run against the **dev** environment.

```bash
# Run all tests
pytest

# Run with Makefile
make test

# Run only smoke tests
pytest -m smoke

# Run specific feature
pytest tests/test_users.py
```

### Configuration & Environments
To switch environments, set the `TARGET_ENV` variable.
Current options: `dev`, `staging`.

```bash
# Linux / Mac
TARGET_ENV=staging pytest

# Windows PowerShell
$env:TARGET_ENV="staging"; pytest
```

Credentials (like `API_TOKEN`) should be set via environment variables. See `.env.example`.

### Generating Reports
HTML reports are generated automatically in `.artifacts/report.html`.
```bash
pytest --html=.artifacts/report.html
```

## Design Decisions
- **Requests vs Httpx**: Chosen `requests` for simplicity and vast ecosystem support, as async was not a hard requirement.
- **Pydantic**: For declarative and robust data validation.
- **Pytest**: The de-facto standard for Python testing with powerful fixture system.
- **Config**: Hybrid approach (YAML for static config, ENV for secrets/overrides) ensures security and flexibility.

## Roadmap
1. [ ] Add Docker support for running tests in isolated container.
2. [ ] Integrate `Allure` reporting for more detailed historical trends.
3. [ ] Add `pre-commit` hooks implementation.
4. [ ] Implement AsyncClient using `httpx` for high-concurrency performance tests.
5. [ ] Add contract testing integration (e.g., Pact).
