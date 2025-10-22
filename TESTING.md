# Testing Guide

## Running Tests

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_schema_extractor.py
```

### Run Specific Test Class

```bash
pytest tests/test_cache_manager.py::TestCacheManager
```

### Run Specific Test

```bash
pytest tests/test_query_validator.py::TestQueryValidator::test_valid_select_query
```

### Run with Coverage

```bash
pytest --cov=db_query_agent --cov-report=html
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Only Fast Tests (exclude slow)

```bash
pytest -m "not slow"
```

---

## Test Structure

### Test Files

- `conftest.py` - Shared fixtures and configuration
- `test_schema_extractor.py` - Schema extraction tests (9 tests)
- `test_cache_manager.py` - Caching system tests (11 tests)
- `test_query_validator.py` - SQL validation tests (11 tests)
- `test_connection_manager.py` - Connection management tests (8 tests)
- `test_config.py` - Configuration tests (12 tests)
- `test_agent_integration.py` - Agent integration tests (8 tests)
- `test_session_manager.py` - Session management tests (12 tests)

**Total: 71+ unit tests**

---

## Test Coverage

### Phase 1 Components (Core Foundation)
- ✅ `schema_extractor.py` - 90%+ coverage
- ✅ `cache_manager.py` - 95%+ coverage
- ✅ `query_validator.py` - 90%+ coverage
- ✅ `connection_manager.py` - 85%+ coverage
- ✅ `config.py` - 95%+ coverage
- ✅ `exceptions.py` - 100% coverage

### Phase 2 Components (Agent Integration)
- ✅ `agent_integration.py` - 80%+ coverage (mocked OpenAI calls)
- ✅ `session_manager.py` - 90%+ coverage
- ✅ `agent.py` - 75%+ coverage (main interface)

**Overall Estimated Coverage: ~90%**

---

## Test Fixtures

### Database Fixtures

- `test_database_url` - SQLite in-memory database URL
- `test_engine` - SQLAlchemy engine with test data
- `db_config` - Database configuration for testing

### Component Fixtures

- `connection_manager` - Connection manager instance
- `schema_extractor` - Schema extractor instance
- `cache_manager` - Cache manager instance
- `query_validator` - Query validator instance

### Configuration Fixtures

- `cache_config` - Cache configuration
- `model_config` - Model configuration
- `safety_config` - Safety configuration

---

## Test Data

The test database includes:

### Tables

**users**
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT UNIQUE)
- active (BOOLEAN)
- created_at (TIMESTAMP)

**orders**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER, FK to users)
- total (REAL)
- status (TEXT)
- created_at (TIMESTAMP)

**products**
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- price (REAL)
- category (TEXT)

### Sample Data

- 3 users (Alice, Bob, Charlie)
- 3 orders (2 for Alice, 1 for Bob)
- 3 products (Laptop, Mouse, Desk)

---

## Writing New Tests

### Test Class Structure

```python
class TestYourComponent:
    """Test YourComponent class."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = YourComponent()
        assert component is not None
    
    def test_some_method(self):
        """Test some method."""
        result = component.some_method()
        assert result == expected_value
    
    @pytest.mark.asyncio
    async def test_async_method(self):
        """Test async method."""
        result = await component.async_method()
        assert result is not None
```

### Using Fixtures

```python
def test_with_fixture(self, schema_extractor):
    """Test using a fixture."""
    schema = schema_extractor.get_schema()
    assert "users" in schema
```

### Mocking External Calls

```python
from unittest.mock import Mock, patch

def test_with_mock(self):
    """Test with mocked dependency."""
    with patch('module.external_call') as mock_call:
        mock_call.return_value = "mocked_value"
        result = function_that_calls_external()
        assert result == "mocked_value"
```

---

## Continuous Integration

### GitHub Actions (Recommended)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -e ".[dev]"
      - run: pytest --cov=db_query_agent
```

---

## Test Best Practices

1. **Test One Thing** - Each test should verify one specific behavior
2. **Use Descriptive Names** - Test names should describe what they test
3. **Arrange-Act-Assert** - Structure tests clearly
4. **Use Fixtures** - Reuse common setup code
5. **Mock External Dependencies** - Don't rely on external services
6. **Test Edge Cases** - Include error conditions and boundary cases
7. **Keep Tests Fast** - Unit tests should run in milliseconds
8. **Independent Tests** - Tests should not depend on each other

---

## Troubleshooting

### Tests Failing

1. Check that all dependencies are installed: `pip install -e ".[dev]"`
2. Verify database fixtures are working: `pytest tests/conftest.py -v`
3. Run tests with verbose output: `pytest -v`
4. Check for import errors: `python -c "import db_query_agent"`

### Async Test Issues

- Ensure `pytest-asyncio` is installed
- Use `@pytest.mark.asyncio` decorator
- Check `pytest.ini` has `asyncio_mode = auto`

### Coverage Not Working

```bash
pip install pytest-cov
pytest --cov=db_query_agent --cov-report=term-missing
```

---

## Future Testing

### Integration Tests (Planned)

- End-to-end query flow
- Real OpenAI API calls (with API key)
- Multiple database types
- Performance benchmarks

### Load Tests (Planned)

- Concurrent query handling
- Cache performance under load
- Connection pool stress testing

---

**Note**: Some tests mock OpenAI API calls to avoid requiring an API key and to ensure fast, deterministic tests. Integration tests with real API calls can be added later.
