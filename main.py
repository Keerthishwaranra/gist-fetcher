from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import Response
import httpx
import cachetools
import orjson

app = FastAPI()
gist_cache = cachetools.TTLCache(maxsize=500, ttl=300)  # 5-min cache, 500 entries

@app.get("/{username}")
async def get_gists(
    username: str,
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(30, ge=1, le=100, description="Items per page")
):
    cache_key = f"{username}-{page}-{per_page}"
    
    # Return cached response if available
    if cache_key in gist_cache:
        return Response(content=orjson.dumps(gist_cache[cache_key], option=orjson.OPT_INDENT_2), media_type="application/json")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.github.com/users/{username}/gists",
                params={"page": page, "per_page": per_page},
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            response.raise_for_status()
            
            # Store in cache and return
            gist_data = response.json()
            gist_cache[cache_key] = gist_data
            return Response(content=orjson.dumps(gist_data, option=orjson.OPT_INDENT_2), media_type="application/json")
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="GitHub API error")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Error connecting to GitHub API")
