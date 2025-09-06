# npl-api
# Advanced NLP API

A high-performance RESTful API for Natural Language Processing tasks and psychological response generation, built with FastAPI.

## 🌟 Features

- **Sentiment Analysis**: Analyze the sentiment of input text
- **Entity Recognition**: Extract named entities from text
- **Text Summarization**: Generate concise summaries of text
- **Psychological Responses**: Access a database of psychologist-style responses
- **Multi-language Support**: Includes translation capabilities
- **Filtering & Search**: Filter responses by input/output text
- **RESTful API**: Fully documented OpenAPI/Swagger interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/advanced-nlp-api.git
   cd advanced-nlp-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Start the server:
   ```bash
   uvicorn advanced_api:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Endpoints

### Psychological Responses
- `GET /` - Welcome message
- `GET /responses` - Get all responses with optional filtering
- `GET /responses/random` - Get a random response
- `GET /responses/{response_id}` - Get a specific response by ID
- `GET /responses/happy` - Get happy responses
- `GET /responses/sad` - Get sad responses

### NLP Endpoints
- `POST /analyze/sentiment` - Analyze sentiment of text
- `POST /analyze/entities` - Extract named entities from text
- `POST /summarize` - Generate a summary of text
- `GET /translate` - Translate text to another language
- `POST /qa` - Get answers to questions about text

## 🤖 Example Usage

### Using cURL

```bash
# Get a random response
curl -X 'GET' \
  'http://localhost:8000/responses/random' \
  -H 'accept: application/json'

# Analyze sentiment
curl -X 'POST' \
  'http://localhost:8000/analyze/sentiment' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "I love this API! It's amazing!"}'
```

### Using Python

```python
import requests

# Get a random happy response
response = requests.get("http://localhost:8000/responses/random")
print(response.json())

# Analyze text sentiment
data = {"text": "I'm feeling great today!"}
response = requests.post("http://localhost:8000/analyze/sentiment", json=data)
print(response.json())
```

## 🛠️ Development

### Running Tests
```bash
# Run tests (add your test commands here)
# pytest tests/
```

### Code Style
This project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- NLP powered by [spaCy](https://spacy.io/)
- Psychological responses dataset (custom)

## 📬 Contact

For questions or feedback, please open an issue on GitHub.

Bhupesh Joshi 
https://www.linkedin.com/in/bhupesh-joshi-profile/
bhupesh.coding@gmail.com
