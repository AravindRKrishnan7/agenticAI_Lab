import os, json
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --- Part A: ask for JSON, then try to parse it ---
text = "Aravind is a 22-year-old final-year student from Kochi who loves building AI agents."

r = client.chat.completions.create(
    model="gemini-2.5-flash",
    temperature=0,
    messages=[
        {"role": "system", "content": "You extract data. Respond ONLY with a JSON object, nothing else."},
        {"role": "user", "content": f"Extract name, age, city, and interest from: {text}"}
    ],
)

raw = r.choices[0].message.content
print("=== RAW model output ===")
print(repr(raw))   # repr reveals hidden characters (newlines, code fences) that break parsing

print("\n=== Trying to parse the RAW output directly ===")
try:
    data = json.loads(raw)
    print("Parsed OK! Name is:", data["name"])
except json.JSONDecodeError as e:
    print("PARSE FAILED:", e)


# --- Part B: break it ON PURPOSE ---
# Models often add chatter before the JSON. json.loads needs PURE JSON, so this crashes.
messy = 'Sure! Here is the JSON you asked for: {"name": "Aravind", "age": 22}'

print("\n=== Parsing messy output (deliberately broken) ===")
try:
    data = json.loads(messy)
    print("Parsed:", data)
except json.JSONDecodeError as e:
    print("PARSE FAILED (as expected):", e)


# --- Part C: THE FIX — strip the code fences, then parse ---
fence = "`" * 3   # three backticks, built safely

print("\n=== Cleaning the fences, then parsing ===")
cleaned = raw.strip()
if cleaned.startswith(fence):
    cleaned = cleaned.strip("`").strip()      # remove backticks from both ends
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()         # drop the leading "json" label

data = json.loads(cleaned)
print("Parsed OK! Interest is:", data["interest"])