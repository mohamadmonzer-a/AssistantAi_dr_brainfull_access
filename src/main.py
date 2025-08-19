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
