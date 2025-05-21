from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import re
import requests
from openai import OpenAI
from openai.types.chat import ChatCompletion

from config import DB_CONFIG, OLLAMA_URL, LOCAL_MODEL, OPENAI_MODEL
from metadata import get_table_schema
from dotenv import load_dotenv
load_dotenv()

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request & response models
class ChatRequest(BaseModel):
    prompt: str
    model: str

class QueryResult(BaseModel):
    columns: list
    rows: list
    html: str = None

def generate_html_table(columns, rows):
    model_style = "color: #1fa105; font-size: 13px; font-style: italic;"
    table_style = "border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 12px;"
    th_style = "border: 1px solid #ccc; padding: 8px 11px; text-align: left; background-color: #f4f4f4; font-weight: bold;"
    td_style = "border: 1px solid #ccc; padding: 8px 11px; text-align: left;"
    tr_even_style = "background-color: #fafafa;"

    html = f"<p>Here is the response by <span style='{model_style}'> {selected_model} </span></p> <br/><table style='{table_style}'>"
    html += "<thead><tr>"
    for col in columns:
        html += f"<th style='{th_style}'>{col}</th>"
    html += "</tr></thead>"

    html += "<tbody>"
    for i, row in enumerate(rows):
        row_style = tr_even_style if i % 2 == 1 else ""
        html += f"<tr style='{row_style}'>"
        for col in columns:
            html += f"<td style='{td_style}'>{row.get(col, '')}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

@app.get("/")
def read_root():
    return "App is running!"


@app.post("/api/query", response_model=QueryResult)
async def handle_query(chat_request: ChatRequest):
    global selected_model
    # print(chat_request.model)

    try:
        schema_text = get_table_schema()
        full_prompt = (
            f"{schema_text}\n\n"
            f"User request: {chat_request.prompt}\n\n"
            f"Write a valid PostgreSQL SELECT SQL query for the 'survey' table based on the user request and only valid column names.\n"
            f"It is just one table containing all data and does not need any JOIN. There are NULL values in the survey table.\n"
            f"Just generate the SQL. No explanation."
        )

        # 🧠 Choose model based on user selection
        if chat_request.model == "local":
            # Call Ollama
            ollama_data = {
                "model": LOCAL_MODEL,
                "prompt": full_prompt,
                "stream": False
            }

            response = requests.post(
                OLLAMA_URL,
                json=ollama_data,
                headers={"Content-Type": "application/json"},
                timeout=60
            )

            response.raise_for_status()

            raw_response = response.json().get("response", "")

        else:
            # old code gpt api
            response: ChatCompletion = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a PostgreSQL expert."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0
            )

            raw_response = response.choices[0].message.content.strip()

        if (chat_request.model=="local"):
            selected_model= LOCAL_MODEL
        else:
            selected_model = OPENAI_MODEL   

        # same logic for both local and gpt servise:
        match = re.search(r"```sql\s+(.*?)\s+```", raw_response, re.DOTALL)
        if match:
            ai_sql = match.group(1).strip()
        else:
            select_match = re.search(r"(SELECT\s+.+?;)", raw_response, re.IGNORECASE | re.DOTALL)
            if select_match:
                ai_sql = select_match.group(1).strip()
            else:
                raise ValueError(f"Invalid SQL generated: {raw_response}")

        if not ai_sql.lower().startswith("select"):
            raise ValueError(f"Invalid SQL generated: {ai_sql}")

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        print("Extracted SQL by", chat_request.model, ":\n", ai_sql)
        cursor.execute(ai_sql)

        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for k, v in dict(row).items():
                if isinstance(v, (int, float)):
                    row_dict[k] = round(v, 1)
                else:
                    row_dict[k] = v
            rows.append(row_dict)

        if len(rows) > 50:
            rows = rows[:50]

        columns = list(rows[0].keys()) if rows else []
        html_table = generate_html_table(columns, rows)

        cursor.close()
        conn.close()

        return QueryResult(columns=columns, rows=rows, html=html_table)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
