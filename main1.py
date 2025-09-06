from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import random

app = FastAPI(title="Psychologist Responses API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_unique_responses():
    with open('psychologist_responses_10k.json') as f:
        data = json.load(f)
    seen = set()
    unique_data = []
    for item in data:
        output = item.get('output')
        if output and output not in seen:
            seen.add(output)
            unique_data.append(item)
    return unique_data

# Load data
responses = load_unique_responses()

def filter_responses(
    responses: List[dict],
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
) -> List[dict]:
    """Filter responses by input and/or output text"""
    filtered = responses
    if input_text:
        input_text = input_text.lower()
        filtered = [r for r in filtered if input_text in r['input'].lower()]
    if output_text:
        output_text = output_text.lower()
        filtered = [r for r in filtered if output_text in r['output'].lower()]
    return filtered

@app.get("/")
async def root():
    return {"message": "Welcome to Psychologist Responses API"}

@app.get("/responses")
async def get_responses(
    limit: int = 10,
    skip: int = 0,
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
):
    """
    Get responses with optional filtering by input and/or output text
    """
    filtered = filter_responses(responses, input_text, output_text)
    return filtered[skip:skip + limit]

@app.get("/responses/random")
async def get_random_response(
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
):
    """
    Get a random response, optionally filtered by input and/or output text
    """
    filtered = filter_responses(responses, input_text, output_text)
    if not filtered:
        raise HTTPException(status_code=404, detail="No matching responses found")
    return random.choice(filtered)

@app.get("/responses/{response_id}")
async def get_response(response_id: str):
    """Get a specific response by ID"""
    for r in responses:
        if r['id'] == response_id:
            return r
    raise HTTPException(status_code=404, detail="Response not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
