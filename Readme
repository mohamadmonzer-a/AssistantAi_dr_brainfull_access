Got it 👍 — the link I gave is only inside my sandbox, you can’t fetch it directly.
I’ll give you the full ZIP file contents here instead so you can recreate it locally.


---

📂 Project: supabase_ai_agent

1. requirements.txt

openai
supabase
python-dotenv
psycopg2-binary


---

2. .env.example

SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=sk-xxxx


---

3. src/db.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_sql(query: str):
    """Run raw SQL on Supabase via a custom function."""
    try:
        result = supabase.rpc("run_sql", {"query": query}).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def fuzzy_search(table: str, first_name: str, last_name: str):
    """Search with fuzzy matching using pg_trgm extension"""
    query = f"""
        SELECT id, first_name, last_name
        FROM {table}
        WHERE similarity(first_name, '{first_name}') > 0.3
          AND similarity(last_name, '{last_name}') > 0.3
        ORDER BY similarity(first_name, '{first_name}') DESC,
                 similarity(last_name, '{last_name}') DESC
        LIMIT 10;
    """
    return run_sql(query)


---

4. src/agent.py

import os
from openai import OpenAI
from db import run_sql, fuzzy_search

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(prompt: str):
    """Ask OpenAI to interpret user command"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Supabase assistant with SQL powers."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]


---

5. src/main.py

from agent import ask_ai
from db import run_sql, fuzzy_search

def main():
    print("🤖 Supabase AI Agent Ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Fuzzy search
        if "find person" in user_input.lower():
            parts = user_input.split()
            if len(parts) >= 3:
                first, last = parts[-2], parts[-1]
                results = fuzzy_search("people", first, last)
                if results and len(results) > 1:
                    print(f"⚠️ Found {len(results)} matches:")
                    for r in results:
                        print(f"- {r['first_name']} {r['last_name']} (id: {r['id']})")
                    continue
                else:
                    print("✅ Result:", results)
                    continue

        # Direct SQL
        if user_input.lower().startswith("sql:"):
            query = user_input[4:].strip()
            result = run_sql(query)
            print("🗄️ Result:", result)
            continue

        # AI-driven
        result = ask_ai(user_input)
        print("AI:", result)

if __name__ == "__main__":
    main()


---

6. schema.sql

-- Enable fuzzy text search
create extension if not exists pg_trgm;

-- Custom function to run raw SQL (be careful!)
create or replace function run_sql(query text)
returns setof json as $$
begin
  return query execute query;
end;
$$ language plpgsql security definer;


---

🚀 How to run

git clone <your-new-repo>
cd supabase_ai_agent
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # and edit values
python src/main.py


---

👉 Do you want me to generate a Base64-encoded zip file that you can copy & decode locally into supabase_ai_agent.zip so you don’t have to rebuild each file manually?

