# FastAPI GitHub Gists Service

## Overview
This is a FastAPI-based web service that fetches public gists from GitHub for a given username. It implements caching using `cachetools` to optimize API calls and provides robust error handling.

## Features
- Fetches public gists of a specified GitHub user.
- Supports pagination via `page` and `per_page` query parameters.
- Implements caching with `cachetools.TTLCache` to reduce redundant API requests.
- Includes comprehensive test cases with `pytest` and `respx` for mocking HTTP requests.

## Installation
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <repo_name>
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application
### Locally
Start the FastAPI server using Uvicorn:
```sh
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Using Docker
Build and run the Docker container:
```sh
docker build -t fastapi-gists .
docker run -p 8080:8080 fastapi-gists
```

## API Endpoints
### Get User Gists
```
GET /{username}
```
#### Query Parameters:
- `page` (int, default: 1) – Page number for pagination.
- `per_page` (int, default: 30, max: 100) – Number of gists per page.

#### Example Request:
```sh
curl -X GET "http://localhost:8080/octocat?page=1&per_page=5"
```

#### Example Response:
```json
[
  {
    "id": "123",
    "description": "Example gist"
  }
]
```

## Running Tests
Run the test suite using `pytest`:
```sh
pytest test_main.py
```

## Technologies Used
- **FastAPI** - Web framework for building APIs.
- **Uvicorn** - ASGI server for running FastAPI applications.
- **httpx** - Async HTTP client for API requests.
- **cachetools** - In-memory caching to optimize API calls.
- **orjson** - High-performance JSON parsing and serialization.
- **pytest & respx** - Unit testing and HTTP request mocking.
- **Docker** - Containerization for easy deployment.

## License
This project is licensed under the MIT License.


