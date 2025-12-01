"""
Test suite for Flask application.
Uses pytest with detailed assertion messages for better CI/CD error reporting.
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for application health and basic endpoints."""
    
    def test_hello_world_status_code(self, client):
        """
        Test: Root endpoint returns HTTP 200 OK
        Endpoint: GET /
        Expected: Status code 200
        """
        response = client.get('/')
        assert response.status_code == 200, \
            f"Expected status 200, got {response.status_code}. " \
            f"Response body: {response.data.decode('utf-8')}"
    
    def test_hello_world_content(self, client):
        """
        Test: Root endpoint returns 'Hello' in response
        Endpoint: GET /
        Expected: Response contains 'Hello'
        """
        response = client.get('/')
        response_text = response.data.decode('utf-8')
        assert 'Hello' in response_text, \
            f"Expected 'Hello' in response, got: '{response_text}'"
    
    def test_hello_world_content_type(self, client):
        """
        Test: Root endpoint returns correct content type
        Endpoint: GET /
        Expected: Content-Type is text/html
        """
        response = client.get('/')
        content_type = response.content_type
        assert 'text/html' in content_type, \
            f"Expected 'text/html' content type, got: '{content_type}'"


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_not_found_returns_404(self, client):
        """
        Test: Non-existent endpoint returns HTTP 404
        Endpoint: GET /nonexistent
        Expected: Status code 404
        """
        response = client.get('/nonexistent')
        assert response.status_code == 404, \
            f"Expected status 404, got {response.status_code}"
    
    def test_method_not_allowed(self, client):
        """
        Test: POST to root endpoint returns HTTP 405
        Endpoint: POST /
        Expected: Status code 405 Method Not Allowed
        """
        response = client.post('/')
        assert response.status_code == 405, \
            f"Expected status 405, got {response.status_code}"


# Uncomment to intentionally fail tests for CI/CD testing
# class TestIntentionalFailures:
#     """Intentional failures for CI/CD testing."""
#     
#     def test_always_fails(self, client):
#         """This test always fails."""
#         assert False, "Intentional failure: test_always_fails in test_app.py:72"
#     
#     def test_wrong_content(self, client):
#         """This test expects wrong content."""
#         response = client.get('/')
#         assert 'Goodbye' in response.data.decode('utf-8'), \
#             "Expected 'Goodbye' but got 'Hello'"
