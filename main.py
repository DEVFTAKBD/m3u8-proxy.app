import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from cors import add_cors

# Get environment variables
enable_docs = os.getenv("documentation", "false").lower() == "true"
docs_url = os.getenv('docs_url', '/docs') if enable_docs else None
redoc_url = os.getenv('redoc_url', '/redoc') if enable_docs else None

allow_no_url_param_also = os.getenv("no_url_param", "false").lower() == "true"

# Setup FastAPI
app = FastAPI(openapi_url=None, docs_url=docs_url, redoc_url=redoc_url)
default_port = 5010

if enable_docs:
    @app.get('/')
    async def home(_: Request):
        return RedirectResponse('/docs')

# Get allowed origins for CORS
allowed_origins = os.getenv("origins", "*")
if not allowed_origins:
    allowed_origins = "*"

# Set the port (default is 5010 if not specified or if the env variable is invalid)
try:
    port = int(os.getenv("port", default_port))
except ValueError:
    print(f"Invalid 'port' environment variable, using default port {default_port}.")
    port = default_port

# Set up CORS
add_cors(app, allowed_origins, allow_no_url_param_also)

# Run the app
if __name__ == '__main__':
    print(f"Starting FastAPI server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
