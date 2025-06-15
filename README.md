A lightweight FastAPI backend for AI applications for natural language to SQL statement, using local Ollama models or ChatGPT API connected to PostgreSQL.

## Project Setup

```sh
pip install -r requirements.txt
```
## sample config

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "llama3.2:latest"  # Your local Ollama model name

DB_CONFIG = {
    "dbname": "dbname",
    "user": "username",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

OPENAI_MODEL = "gpt-xyz" 
```

## Running Locally

```sh
uvicorn main:app --reload
```
