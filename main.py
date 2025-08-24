# app/main.py

import os
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

# Environment (default: production)
#ENV = os.getenv("ENV", "production")
ENV="dev"
# Disable docs in production
app = FastAPI(
    title="My Secure FastAPI App",
    docs_url="/docs" if ENV == "dev" else None,
    redoc_url="/redoc" if ENV == "dev" else None,
    openapi_url="/openapi.json" if ENV == "dev" else None
)

# Hide "server: uvicorn" header
class HideServerHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if "server" in response.headers:
            del response.headers["server"]
        return response

app.add_middleware(HideServerHeaderMiddleware)

# Allow only your domain (adjust domain names as needed)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["52.91.58.123","127.0.0.1"]
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS (restrict to your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["52.91.58.123","127.0.0.1"],  # set to "*" only for testing
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Example root route
@app.get("/")
async def root():
    return {"message": "Secure FastAPI is running!"}

# Example protected API route
@app.get("/api/data")
async def get_data():
    return {"status": "ok", "data": [1, 2, 3]}

# Custom error handler (example)
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "The resource was not found."}
    )
