# Psychologist Responses API

API for accessing psychologist responses to various mental health inputs.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Get All Responses
```
GET /responses
```

**Query Parameters:**
- `limit` (optional, default: 10): Number of responses to return
- `skip` (optional, default: 0): Number of responses to skip
- `input_text` (optional): Filter responses by input text (case-insensitive)
- `output_text` (optional): Filter responses by output text (case-insensitive)

**Example:**
```
GET /responses?input_text=afraid&limit=5
```

### 2. Get Random Response
```
GET /responses/random
```

**Query Parameters:**
- `input_text` (optional): Filter by input text
- `output_text` (optional): Filter by output text

**Example:**
```
GET /responses/random?output_text=happiness
```

### 3. Get Response by ID
```
GET /responses/{response_id}
```

**Example:**
```
GET /responses/42
```

## Example Requests

### Filter responses by input text:
```bash
curl "http://localhost:8000/responses?input_text=afraid"
```

### Get a random response with specific output:
```bash
curl "http://localhost:8000/responses/random?output_text=happiness"
```

https://api-nlp-six.vercel.app/responses/random?output_text=happiness
### Combine filters with pagination:
```bash
curl "http://localhost:8000/responses?input_text=afraid&output_text=strengths&limit=3&skip=0"
```


<!-- 100 afraid -->

http://localhost:8000/responses?input_text=afraid&output_text=strengths&limit=100&skip=0

https://api-nlp-six.vercel.app/responses?input_text=afraid&output_text=strengths&limit=1000&skip=0

fastapi>=0.95.0
uvicorn[standard]>=0.21.1
spacy>=3.5.0
python-multipart>=0.0.6
python-dotenv>=0.19.0

for killing port
lsof -i :8001

kill <PID>
# or if it doesn't work:
kill -9 <PID>

check the size of data:
ls -lh psychologist_responses_10k.json
-rw-r--r--@ 1 joshi  staff   1.6M Sep  5 17:37 psychologist_responses_10k.json


size of virtaul env

du -sh .venv/
219M    .venv/

Check the size of node_modules:
du -sh node_modules/


Check for large files in your project:
find . -type f -size +10M -exec ls -lh {} \;


https://api-nlp-six.vercel.app/responses?input_text=afraid&output_text=strengths&limit=1000&skip=0


echo "# npl-api" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/bhupeshcoding/npl-api.git
git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/bhupeshcoding/npl-api.git
git branch -M main
git push -u origin main
