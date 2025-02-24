# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app
import cachetools
import orjson
import httpx
import respx

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404  # No root endpoint exists

@respx.mock
def test_get_gists_success():
    # Mock GitHub API response
    mock_gists = [{"id": "123", "description": "test gist"}]
    mock_route = respx.get("https://api.github.com/users/validuser/gists").mock(
        return_value=httpx.Response(200, json=mock_gists)
    )

    response = client.get("/validuser?page=1&per_page=30")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert orjson.loads(response.content) == mock_gists
    assert mock_route.called

def test_cache_behavior():
    # Clear cache before test
    app.dependency_overrides = {}
    app.extra = {"gist_cache": cachetools.TTLCache(maxsize=500, ttl=300)}

    with respx.mock:
        mock_route = respx.get("https://api.github.com/users/cacheduser/gists").mock(
            return_value=httpx.Response(200, json=[])
        )
        
        # First request - should call GitHub API
        response1 = client.get("/cacheduser")
        assert mock_route.call_count == 1
        
        # Second request - should use cache
        response2 = client.get("/cacheduser")
        assert mock_route.call_count == 1
        assert response1.content == response2.content

@respx.mock
def test_github_api_error():
    respx.get("https://api.github.com/users/erroruser/gists").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    
    response = client.get("/erroruser")
    assert response.status_code == 404
    assert response.json()["detail"] == "GitHub API error"

@respx.mock
def test_connection_error():
    respx.get("https://api.github.com/users/networkerror/gists").mock(
        side_effect=httpx.RequestError("Connection failed")
    )
    
    response = client.get("/networkerror")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error connecting to GitHub API"

def test_query_parameter_validation():
    # Test invalid page parameter
    response = client.get("/testuser?page=0")
    assert response.status_code == 422
    assert "page" in response.text.lower()

    # Test invalid per_page parameter
    response = client.get("/testuser?per_page=101")
    assert response.status_code == 422
    assert "per_page" in response.text.lower()

def test_response_formatting():
    test_data = {"key": "value", "nested": {"id": 123}}
    with respx.mock:
        respx.get("https://api.github.com/users/formatuser/gists").mock(
            return_value=httpx.Response(200, json=test_data)
        )
        
        response = client.get("/formatuser")
        formatted_json = orjson.dumps(test_data, option=orjson.OPT_INDENT_2).decode()
        assert response.content.decode() == formatted_json
