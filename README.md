# Mock Flask Improvements for Better Jenkins CI/CD Output

This folder contains improved files for your `mock_flask` repository that produce cleaner, more actionable CI/CD logs.

## What's Improved

### 1. `Jenkinsfile` - Enhanced Pipeline with Clean Output

**Key improvements:**
- **Suppressed noise**: Virtualenv activation scripts, pip verbose output, and git operations are hidden
- **Structured sections**: Each stage has clear `===` delimiters for easy parsing
- **Focused lint output**: Uses custom format `[LINT ERROR] file:line:col: CODE - message`
- **Better error handling**: Clear failure messages with common fix suggestions
- **Build summary**: Shows status, duration, and build URL at the end

**Example clean output on failure:**
```
==========================================
LINT CHECK - SYNTAX ERRORS
==========================================
[LINT ERROR] app.py:8:14: E999 - SyntaxError: invalid syntax
    retursn 'Hello, World!'
             ^

==========================================
LINT FAILED - Fix the errors above
==========================================
```

### 2. `test_app.py` - Enhanced Tests with Better Assertions

**Key improvements:**
- **Organized test classes**: `TestHealthCheck` and `TestErrorHandling`
- **Detailed assertion messages**: Shows expected vs actual values
- **Docstrings**: Each test describes endpoint, expected behavior
- **More coverage**: Tests status codes, content, content-type, 404s, 405s

### 3. `app.py` - Fixed Syntax Error

The syntax error (`retursn` → `return`) is fixed.

### 4. `requirements.txt` - Added pytest

Added `pytest>=7.0.0` for testing.

## How to Use

1. **Clone your mock_flask repo** (or navigate to it):
   ```bash
   cd /path/to/mock_flask
   ```

2. **Copy the improved files**:
   ```bash
   cp /path/to/TM/mock_flask_improvements/* .
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Improved CI/CD output with cleaner logs and better tests"
   git push
   ```

4. **Run the Jenkins pipeline** and observe the cleaner logs!

## What Your TM App Now Does

The TM backend (`jenkins_services.py`) now:

1. **Filters noise** - Removes virtualenv scripts, git output, pip messages
2. **Extracts structured errors**:
   - Lint errors: `[{file, line, column, code, message}]`
   - Test failures: `[{file, test, reason}]`
   - Python exceptions: tracebacks with context
3. **Generates summary** - Shows count of each error type
4. **Stores clean logs** - Much smaller than raw logs, only actionable content

### Example Parsed Output

When Jenkins fails, your app will store:

```json
{
  "logs": "==========================================\nLINT CHECK - SYNTAX ERRORS\n==========================================\napp.py:8:14: E999 SyntaxError: invalid syntax\n    retursn 'Hello, World!'\n             ^",
  "summary": "Build: flask-pipeline #35\nResult: FAILURE\nDuration: 12.5s\nErrors: Found 1 error(s), 1 lint error(s)\n\nLint Errors (1):\n  • app.py:8 [E999] SyntaxError: invalid syntax",
  "errors": {
    "lint": [{"file": "app.py", "line": 8, "code": "E999", "message": "SyntaxError: invalid syntax"}],
    "test": []
  }
}
```

## Testing Intentional Failures

To test your CI/CD error analysis, you can:

1. **Introduce a syntax error** in `app.py`:
   ```python
   def hello_world():
       retursn 'Hello, World!'  # typo!
   ```

2. **Uncomment the intentional failures** in `test_app.py`:
   ```python
   class TestIntentionalFailures:
       def test_always_fails(self, client):
           assert False, "Intentional failure"
   ```

3. Push and watch the pipeline fail with clean, parseable output!

## Webhook Note

If your Jenkins webhook to `http://localhost:8000/api/webhooks/jenkins` fails (Connection refused), it means:
- Jenkins is running in Docker but trying to reach `localhost` (which is inside the container)
- **Fix**: Use `http://host.docker.internal:8000/api/webhooks/jenkins` in Jenkins notification config

Or run both Jenkins and your Django backend on the same Docker network.
