---
applyTo:
  - "tests/**/*.py"
---

# Test Code Guidelines

Write focused, readable unit tests that test ONE thing at a time.

## Critical Test Rules

### NO Docstrings in Tests
- Test names must be self-explanatory
- If you need a docstring to explain a test, the test name is wrong
- **NEVER** add docstrings to test functions

```python
# ✓ Good - clear name, no docstring needed
async def test_connect_when_already_connected_raises_connection_error():
    client = CDPClient("ws://localhost")
    await client.connect()

    with pytest.raises(CDPConnectionException, match="Already connected"):
        await client.connect()

# ✗ Bad - unclear name requiring docstring
async def test_connect_error():
    """Test that connecting twice raises an error."""  # Don't do this!
    client = CDPClient("ws://localhost")
    ...
```

### NO Inline Comments
- Code should be self-documenting through clear variable names
- Use well-named variables instead of comments
- Extract complex expressions into named variables

```python
# ✓ Good - self-explanatory
async def test_send_raw_timeout_raises_timeout_error():
    client = CDPClient("ws://localhost", default_timeout=0.1)
    await client.connect()

    with pytest.raises(CDPTimeoutException, match="timed out after 0.1s"):
        await client.send_raw("Page.navigate", {"url": "https://example.com"})

# ✗ Bad - unnecessary comments
async def test_timeout():
    # Create client with short timeout
    client = CDPClient("ws://localhost", default_timeout=0.1)
    # Connect to websocket
    await client.connect()

    # This should timeout because we set timeout to 0.1s
    with pytest.raises(CDPTimeoutException):
        await client.send_raw("Page.navigate", {"url": "https://example.com"})
```

### Always Type Fixtures
- **ALL** fixture parameters must have type hints
- Enables IDE autocomplete and type checking
- Makes test dependencies explicit

```python
# ✓ Good - typed fixture
@pytest.fixture
def websocket_url() -> str:
    return "ws://localhost:9222/devtools"

@pytest.fixture
async def connected_client(websocket_url: str) -> AsyncIterator[CDPClient]:
    async with CDPClient(websocket_url) as client:
        yield client

async def test_send_command(connected_client: CDPClient):
    result = await connected_client.send_raw("Page.navigate")
    assert result is not None

# ✗ Bad - no type hints
@pytest.fixture
def websocket_url():  # Missing return type
    return "ws://localhost:9222/devtools"

@pytest.fixture
async def connected_client(websocket_url):  # Missing parameter type
    async with CDPClient(websocket_url) as client:
        yield client

async def test_send_command(connected_client):  # Missing parameter type
    result = await connected_client.send_raw("Page.navigate")
    assert result is not None
```

## Test Structure

### Follow AAA Pattern
```python
async def test_send_command_success():
    # Arrange - setup test data and mocks
    client = CDPClient("ws://localhost")
    expected_result = {"success": True}

    # Act - execute the code under test
    result = await client.send_raw("Page.navigate", {"url": "https://example.com"})

    # Assert - verify expectations
    assert result == expected_result
```

### Test Naming
- Pattern: `test_<method>_<scenario>_<expected_result>`
- Examples:
  - `test_connect_when_already_connected_raises_error`
  - `test_send_raw_with_valid_params_returns_result`
  - `test_disconnect_cancels_pending_requests`
- Be specific: test name should reveal what's being tested

## Core Principles

### One Assert Per Test
- Each test should verify ONE behavior
- Split into multiple tests if checking multiple scenarios
- Makes failures immediately obvious

```python
# ✓ Good - focused test
async def test_connect_establishes_websocket():
    client = CDPClient("ws://localhost")
    await client.connect()
    assert client.is_connected

async def test_connect_starts_message_loop():
    client = CDPClient("ws://localhost")
    await client.connect()
    assert client._message_loop_task is not None

# ✗ Bad - testing multiple things
async def test_connect():
    client = CDPClient("ws://localhost")
    await client.connect()
    assert client.is_connected  # Testing connection
    assert client._message_loop_task is not None  # Testing task
    assert len(client._pending_requests) == 0  # Testing state
```

### Test Independence
- Each test must run in isolation
- No shared state between tests
- Use fixtures for setup, not module-level variables
- Tests should pass in any order

### Use Fixtures for Setup
```python
@pytest.fixture
def client():
    return CDPClient("ws://localhost", default_timeout=30.0)

@pytest.fixture
async def connected_client():
    async with CDPClient("ws://localhost") as client:
        yield client

async def test_send_raw_requires_connection(client):
    with pytest.raises(CDPConnectionException, match="Not connected"):
        await client.send_raw("Page.navigate")
```

### Mock External Dependencies
- Mock network calls, file I/O, external services
- Use `unittest.mock` or `pytest-mock`
- Don't mock the code under test
- Verify mock calls when testing commands

```python
async def test_connect_establishes_websocket_connection(mocker):
    mock_connect = mocker.patch("websockets.asyncio.client.connect")
    mock_ws = mocker.AsyncMock()
    mock_connect.return_value = mock_ws

    client = CDPClient("ws://localhost")
    await client.connect()

    mock_connect.assert_called_once_with(
        "ws://localhost",
        max_size=100 * 1024 * 1024,
        additional_headers=None,
    )
```

## Test Organization

### Group Related Tests
```python
class TestCDPClientConnection:
    async def test_connect_when_already_connected_raises_error(self):
        ...

    async def test_connect_establishes_websocket(self):
        ...

    async def test_disconnect_closes_websocket(self):
        ...

class TestCDPClientCommands:
    async def test_send_raw_with_params_includes_in_message(self):
        ...

    async def test_send_raw_timeout_raises_timeout_error(self):
        ...
```

### Test File Structure
- Mirror source structure: `pydantic_cpd/client.py` → `tests/test_client.py`
- One test file per source file
- Keep test files focused

## Async Testing
- Use `pytest-asyncio` for async tests
- Mark async tests: `async def test_...`
- Use `await` for async operations
- Clean up resources in fixtures

```python
@pytest.fixture
async def client():
    client = CDPClient("ws://localhost")
    await client.connect()
    yield client
    await client.disconnect()  # Cleanup
```

## What to Test

### Focus on Behavior
- Test public API, not implementation details
- Test error conditions and edge cases
- Test state transitions
- Verify side effects for commands

### Don't Test
- Private methods directly (test through public API)
- Third-party library internals
- Simple getters/setters without logic
- Framework code

## Error Testing
```python
async def test_send_raw_when_disconnected_raises_error():
    client = CDPClient("ws://localhost")

    with pytest.raises(CDPConnectionException, match="Not connected"):
        await client.send_raw("Page.navigate")

async def test_command_error_wraps_cdp_error():
    client = CDPClient("ws://localhost")
    error_data = {"code": -32601, "message": "Method not found"}

    with pytest.raises(CDPCommandException) as exc_info:
        # Setup to trigger error...
        pass

    assert exc_info.value.code == -32601
    assert "Method not found" in str(exc_info.value)
```

## Parametrized Tests
Use for testing same behavior with different inputs:

```python
@pytest.mark.parametrize("url,expected", [
    ("ws://localhost", "ws://localhost"),
    ("ws://localhost:9222", "ws://localhost:9222"),
    ("wss://remote.com/devtools", "wss://remote.com/devtools"),
])
def test_client_stores_url(url, expected):
    client = CDPClient(url)
    assert client.url == expected

@pytest.mark.parametrize("timeout", [10.0, 30.0, 60.0])
async def test_send_raw_respects_timeout(timeout):
    client = CDPClient("ws://localhost", default_timeout=timeout)
    # Test timeout behavior...
```

## Test Data
- Use realistic but minimal test data
- Extract common test data to fixtures or constants
- Don't use production data in tests

```python
# ✓ Good - minimal realistic data
TEST_URL = "ws://localhost:9222/devtools/page/123"
VALID_MESSAGE = {"id": 1, "method": "Page.navigate", "params": {"url": "https://example.com"}}

# ✗ Bad - overly complex test data
COMPLEX_MESSAGE = {
    "id": 123456789,
    "method": "Network.getResponseBody",
    "params": {"requestId": "abc-def-ghi-jkl", "sessionId": "xyz-123-456"},
    "metadata": {"timestamp": 1234567890, "source": "test"},
    # ... lots more fields
}
```

## Mocking Guidelines

### Mock at the Boundary
- Mock external I/O (network, filesystem, database)
- Don't mock business logic
- Keep mocks simple and focused

```python
# ✓ Good - mocking external dependency
async def test_connect_uses_websocket_library(mocker):
    mock_connect = mocker.patch("websockets.asyncio.client.connect")
    client = CDPClient("ws://localhost")
    await client.connect()
    mock_connect.assert_called_once()

# ✗ Bad - mocking internal logic
async def test_process_message(mocker):
    client = CDPClient("ws://localhost")
    mocker.patch.object(client, "_handle_response")  # Don't do this
    await client._process_message("{}")
```

## What Makes a Good Test

A good unit test is:
1. **Fast** - runs in milliseconds
2. **Isolated** - no dependencies on other tests
3. **Repeatable** - same result every time
4. **Self-validating** - pass or fail, no manual inspection
5. **Timely** - written alongside code, not after
6. **Focused** - tests ONE thing clearly

## Red Flags

Avoid:
- Tests with `sleep()` or `time.sleep()`
- Tests that depend on execution order
- Tests that rely on external services
- Tests with too many mocks (indicates design issue)
- Tests that duplicate implementation logic
- Tests that are harder to understand than the code

## Example Good Test

```python
async def test_disconnect_cancels_pending_requests():
    client = CDPClient("ws://localhost")
    await client.connect()

    request_task = asyncio.create_task(
        client.send_raw("Page.navigate", {"url": "https://example.com"})
    )
    await asyncio.sleep(0)

    await client.disconnect()

    with pytest.raises(CDPConnectionException, match="Disconnected"):
        await request_task
```

## Example Bad Test

```python
async def test_everything():  # ✗ Unclear name
    """Test the client works correctly"""  # ✗ Unnecessary docstring
    client = CDPClient("ws://localhost")

    # First connect to the websocket  # ✗ Obvious comment
    await client.connect()
    assert client.is_connected  # ✗ Multiple assertions

    # Now send a command  # ✗ Unnecessary comment
    result = await client.send_raw("Page.navigate")
    assert result  # ✗ Weak assertion

    # Check internal state  # ✗ Testing implementation details
    assert len(client._pending_requests) == 0

    # Finally disconnect  # ✗ Comment stating the obvious
    await client.disconnect()
    assert not client.is_connected  # ✗ Too many concerns
```

**Remember**: Tests are documentation. They should clearly show how the code is meant to be used and what behavior is expected.
