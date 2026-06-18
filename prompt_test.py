import os, time
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# A small helper so we don't repeat the API call 3 times.
# (You'll wrap API calls like this constantly in real agent code.)
def ask(messages):
    r = client.chat.completions.create(
        model="gemini-2.5-flash",
        temperature=0,   # temp 0 on purpose: so differences come from the PROMPT, not randomness
        messages=messages,
    )
    return r.choices[0].message.content


# V1 — vague prompt
print("=== V1: vague ===")
print(ask([{"role": "user", "content": "Explain APIs"}]))
time.sleep(15)

# V2 — specific prompt (added constraints + audience + format)
print("\n=== V2: specific ===")
print(ask([
    {"role": "user", "content": "Explain what an API is to a 10-year-old in exactly 2 sentences, using a restaurant analogy."}
]))
time.sleep(15)

# V3 — same specific prompt, PLUS a system prompt that sets persona + rules
print("\n=== V3: specific + system prompt ===")
print(ask([
    {"role": "system", "content": "You are a witty teacher for absolute beginners. You never use jargon. You always end with a one-line summary that starts with 'TL;DR:'."},
    {"role": "user", "content": "Explain what an API is to a 10-year-old in exactly 2 sentences, using a restaurant analogy."}
]))