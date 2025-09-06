import logging
import json
import random
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import spacy

# ------------------------------------------------------------------------------
# Setup logging
# ------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedNLPApi")

# ------------------------------------------------------------------------------
# Initialize FastAPI app
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Advanced NLP API", 
    description="An advanced API for NLP tasks and psychologist responses", 
    version="1.0.0"
)

# Enable CORS for all origins (development/demo purpose)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Load NLP model (spaCy)
# ------------------------------------------------------------------------------
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Spacy model loaded successfully.")
except Exception as e:
    logger.error("Error loading spacy model: %s", e)
    nlp = None

# ------------------------------------------------------------------------------
# Pydantic models for request and responses
# ------------------------------------------------------------------------------
class NLPRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: float
    label: str

class EntitiesResponse(BaseModel):
    entities: List[Dict[str, Any]]

class SummaryResponse(BaseModel):
    summary: str

# ------------------------------------------------------------------------------
# Psychological Responses Section
# ------------------------------------------------------------------------------
def load_responses():
    logger.info("Step 1: Loading responses from psychologist_responses_10k.json")
    try:
        with open("psychologist_responses_10k.json", "r") as f:
            data = json.load(f)
        logger.info("Step 2: Loaded %d responses", len(data))
        print(f"Loaded {len(data)} responses")
        return data
    except Exception as e:
        logger.error("Error loading responses: %s", e)
        return []

responses = load_responses()
response_map = {str(r.get("id")): r for r in responses if r.get("id") is not None}
logger.info("Step 3: Built response_map with %d entries", len(response_map))

def filter_responses(
    data: List[dict],
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
) -> List[dict]:
    logger.info("Step 4: Starting filtering responses")
    filtered = data
    if input_text:
        input_text_lower = input_text.lower()
        logger.info(" - Filtering by input text: %s", input_text)
        filtered = [r for r in filtered if input_text_lower in r.get("input", "").lower()]
    if output_text:
        output_text_lower = output_text.lower()
        logger.info(" - Filtering by output text: %s", output_text)
        filtered = [r for r in filtered if output_text_lower in r.get("output", "").lower()]
    logger.info("Step 5: Filtering complete; number of responses: %d", len(filtered))
    return filtered

# ------------------------------------------------------------------------------
# Endpoints for Psychological Responses
# ------------------------------------------------------------------------------
@app.get("/", tags=["General"])
def index():
    logger.info("Step 6: GET / endpoint called")
    return {"message": "Welcome to the Advanced NLP API"}

@app.get("/responses", tags=["Psychologist Responses"])
def get_responses(
    limit: int = 10000,
    skip: int = 0,
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
):
    logger.info("Step 7: GET /responses called with limit=%d, skip=%d, input_text=%s, output_text=%s", 
                limit, skip, input_text, output_text)
    filtered = filter_responses(responses, input_text, output_text)
    result = filtered[skip: skip + limit]
    logger.info("Step 8: Returning %d responses", len(result))
    return result

@app.get("/responses/random", tags=["Psychologist Responses"])
def get_random_response(
    input_text: Optional[str] = None,
    output_text: Optional[str] = None,
):
    logger.info("Step 9: GET /responses/random called with input_text=%s, output_text=%s",
                input_text, output_text)
    filtered = filter_responses(responses, input_text, output_text)
    if not filtered:
        logger.error(" - No matching responses found.")
        raise HTTPException(status_code=404, detail="No matching responses found")
    selection = random.choice(filtered)
    logger.info("Step 10: Random response selected: %s", selection)
    return selection

@app.get("/responses/{response_id}", tags=["Psychologist Responses"])
def get_response(response_id: str):
    logger.info("Step 11: GET /responses/%s called", response_id)
    response = response_map.get(response_id)
    if response:
        logger.info(" - Found response: %s", response)
        return response
    logger.error(" - Response not found for id: %s", response_id)
    raise HTTPException(status_code=404, detail="Response not found")

@app.get("/responses/happy", tags=["Psychologist Responses"])
def get_happy_responses(
    limit: int = 10000,
    skip: int = 0,
):
    logger.info("GET /responses/happy endpoint called, filtering by 'happy'")
    # Filter responses that contain the word 'happy' in the output field.
    filtered = filter_responses(responses, output_text="happy")
    result = filtered[skip: skip + limit]
    logger.info("Returning %d happy responses", len(result))
    return result

@app.get("/responses/sad", tags=["Psychologist Responses"])
def get_sad_responses(
    limit: int = 10000,
    skip: int = 0,
):
    logger.info("GET /responses/sad endpoint called, filtering by 'sad'")
    # Filter responses that contain the word 'sad' in the output field.
    filtered = filter_responses(responses, output_text="sad")
    result = filtered[skip: skip + limit]
    logger.info("Returning %d sad responses", len(result))
    return result

# ------------------------------------------------------------------------------
# Advanced NLP Endpoints
# ------------------------------------------------------------------------------

@app.post("/nlu/sentiment", response_model=SentimentResponse, tags=["NLP"])
def analyze_sentiment(request: NLPRequest):
    logger.info("POST /nlu/sentiment called with text: %s", request.text)
    # For demonstration: simulate sentiment analysis with a random score.
    sentiment_score = random.uniform(-1, 1)
    label = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
    logger.info("Sentiment score: %f, label: %s", sentiment_score, label)
    return SentimentResponse(sentiment=sentiment_score, label=label)

@app.post("/nlu/entities", response_model=EntitiesResponse, tags=["NLP"])
def extract_entities(request: NLPRequest):
    logger.info("POST /nlu/entities called with text: %s", request.text)
    if nlp:
        doc = nlp(request.text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        logger.info("Extracted entities: %s", entities)
        return EntitiesResponse(entities=entities)
    logger.error("NLP model not loaded")
    raise HTTPException(status_code=500, detail="NLP model not available")

@app.post("/nlu/summarize", response_model=SummaryResponse, tags=["NLP"])
def summarize_text(request: NLPRequest):
    logger.info("POST /nlu/summarize called with text: %s", request.text)
    # For demonstration: a naive "summarization" that returns the first sentence.
    sentences = request.text.split('.')
    summary = sentences[0].strip() + '.' if sentences and sentences[0] != "" else request.text
    logger.info("Generated summary: %s", summary)
    return SummaryResponse(summary=summary)

@app.get("/nlu/translate", tags=["NLP"])
def translate_text(text: str, target_lang: str = "es"):
    logger.info("GET /nlu/translate called with text: %s, target_lang: %s", text, target_lang)
    # For demonstration: simulate translation by reversing text and appending language code.
    translated = f"{text[::-1]} ({target_lang})"
    logger.info("Translated text: %s", translated)
    return {"translated_text": translated}

@app.post("/nlu/qa", tags=["NLP"])
def question_answer(request: NLPRequest, question: str = Query(...)):
    logger.info("POST /nlu/qa called with context text: %s and question: %s", request.text, question)
    # For demonstration: Search the context for the first sentence containing a word from the question.
    sentences = request.text.split('.')
    answer = "No answer found"
    for sentence in sentences:
        for word in question.split():
            if word.lower() in sentence.lower():
                answer = sentence.strip() or answer
                break
        if answer != "No answer found":
            break
    logger.info("Answer: %s", answer)
    return {"question": question, "answer": answer}

@app.get("/nlu/info", tags=["NLP"])
def get_nlu_info():
    logger.info("GET /nlu/info called")
    info = {
        "version": "1.0",
        "description": "Advanced NLP API with multiple NLP endpoints",
        "endpoints": ["/nlu/sentiment", "/nlu/entities", "/nlu/summarize", "/nlu/translate", "/nlu/qa"]
    }
    logger.info("NLP info: %s", info)
    return info

# ------------------------------------------------------------------------------
# Demo Endpoints to Simulate a Large Codebase
# ------------------------------------------------------------------------------
for i in range(50):
    @app.get(f"/demo/endpoint/{i}", tags=["Demo Endpoints"])
    def demo_endpoint(i=i):
        logger.info("Demo endpoint %d called", i)
        return {"demo": f"This is demo endpoint number {i}"}

# ------------------------------------------------------------------------------
# Additional Utility Functions (simulate helper modules)
# ------------------------------------------------------------------------------
def utility_function_a(x: int, y: int) -> int:
    result = x + y + random.randint(0, 100)
    logger.debug("utility_function_a: %d + %d = %d", x, y, result)
    return result

def utility_function_b(text: str) -> str:
    result = text.upper()[::-1]
    logger.debug("utility_function_b: input: %s, output: %s", text, result)
    return result

def simulate_load():
    logger.info("Starting lengthy simulation of tasks...")
    results = []
    for i in range(100):
        for j in range(100):
            result = utility_function_a(i, j)
            modified = utility_function_b(f"Value {result}")
            results.append(modified)
    logger.info("Simulation complete with %d results", len(results))
    return results

@app.get("/simulate", tags=["Simulation"])
def simulate_tasks():
    logger.info("GET /simulate called")
    results = simulate_load()
    return {"simulation_results": results[:10], "total": len(results)}

# ------------------------------------------------------------------------------
# Main entry point to run the API
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Advanced NLP API Server on port 8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)