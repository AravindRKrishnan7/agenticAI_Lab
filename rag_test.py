import os, time
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def embed(text):
    r = client.embeddings.create(model="gemini-embedding-001", input=text)
    return r.data[0].embedding

def similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    mag_a = sum(x*x for x in a) ** 0.5
    mag_b = sum(y*y for y in b) ** 0.5
    return dot / (mag_a * mag_b)

# 1. Our tiny knowledge base (the "documents")
docs = [
    "The hackathon final submission deadline is July 15th at 11:59 PM.",
    "Teams can have a maximum of 4 members.",
    "The grand prize is 50,000 rupees plus an internship interview.",
    "Projects must use at least one AI/ML component to qualify.",
    "Food and accommodation are provided free to all participants.",
]

# 2. Embed every document once (this is "indexing" your knowledge base)
doc_embeddings = []
for d in docs:
    doc_embeddings.append(embed(d))
    time.sleep(1)            # be gentle on the free-tier rate limit

# 3. The question
question = "How many people can be on my team?"
q_embedding = embed(question)

# 4. RETRIEVE: rank docs by similarity, grab the closest one
scores = [similarity(q_embedding, de) for de in doc_embeddings]
best = scores.index(max(scores))          # index of the highest-scoring doc
retrieved = docs[best]

print("Question :", question)
print("Retrieved:", retrieved)
print("Score    :", round(max(scores), 3), "\n")

# 5. GENERATE: answer using ONLY the retrieved doc, and cite it
messages = [
    {"role": "system", "content":
        "Answer using ONLY the provided context. If the answer isn't in the context, "
        "say you don't know. End by quoting the exact sentence you used as your source."},
    {"role": "user", "content": f"Context: {retrieved}\n\nQuestion: {question}"}
]
r = client.chat.completions.create(model="gemini-2.5-flash", temperature=0, messages=messages)
print("Answer:", r.choices[0].message.content)