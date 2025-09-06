from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetlifyAPI")

# Import your existing FastAPI app
from advanced_api import app as fastapi_app

# Create a new FastAPI instance for Netlify
app = FastAPI(
    title="NLP API Service",
    description="Advanced NLP API deployed on Netlify Functions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from your existing FastAPI app
app.include_router(fastapi_app.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the NLP API Service",
        "docs": "/docs",
        "endpoints": [
            "/api/responses",
            "/api/responses/random",
            "/api/responses/{response_id}",
            "/api/nlu/sentiment",
            "/api/nlu/entities",
            "/api/nlu/summarize",
            "/api/nlu/translate",
            "/api/nlu/qa",
            "/api/simulate"
        ]
    }

# Create handler for Netlify
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    logger.info("Starting API server on port 8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)