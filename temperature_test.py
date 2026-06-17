import os
import time
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

prompt = "Give me a one-sentence tagline for a coffee shop run by cats."

for temp in [0, 1]:
    print(f"\n===== temperature {temp} =====")
    for run in range(3):
        r = client.chat.completions.create(
            model="gemini-2.5-flash",
            temperature=temp,
            messages=[{"role": "user", "content": prompt}],
        )
        print(f"run {run+1}: {r.choices[0].message.content}")
        time.sleep(15)   # free tier = 5 req/min, so wait between calls