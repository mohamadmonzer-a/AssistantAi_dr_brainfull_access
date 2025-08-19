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
