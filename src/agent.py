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
