import os 
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

print(ask_ai("What is RAG in one sentence?"))
print(ask_ai("Name three Indian cities."))