A lightweight demo of FastAPI backend for AI applications.

## Project Setup

```sh
pip install -r requirements.txt
```
## sample config

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "llama3.2:latest"  # Your local Ollama model name

DB_CONFIG = {
    "dbname": "jmmi",
    "user": "usernae",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

OPENAI_MODEL = "gpt-4o-mini" 

### Running Locally

```sh
uvicorn main:app --reload
```
