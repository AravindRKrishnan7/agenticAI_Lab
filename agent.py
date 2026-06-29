import os 
import json
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
def ask_ai(prompt):
    r = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return r.choices[0].message.content

def ask_ai_json(prompt):
    r = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You reply ONLY with valid JSON. No markdown, no explanation."},
            {"role": "user", "content": prompt}
        ],
    )
    raw = r.choices[0].message.content
    return json.loads(raw)

print(ask_ai("What is RAG in one sentence?"))
print(ask_ai("Name three Indian cities."))

cities = ask_ai_json("Give me 3 Indian cities with their population. Keys: city, population.")
for c in cities:
    print(c["city"], "-", c["population"])
print(cities)
print(type(cities))