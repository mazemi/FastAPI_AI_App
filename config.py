OLLAMA_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "llama3.2:latest"

DB_CONFIG = {
    "dbname": "jmmi",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432
}

OPENAI_MODEL = "gpt-4o-mini"    # $0.30 per 1M tokens
# OPENAI_MODEL = "GPT-4.1"      #$2.00 per 1M input tokens; $8.00 per 1M output tokens
# OPENAI_MODEL = "gpt-4o"       #$5.00 per 1M tokens.