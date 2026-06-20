import os, json
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 1. The REAL function — only YOUR code can run this, never the model
def multiply(a, b):
    return a * b

# 2. The TOOL MENU shown to the model: name, what it does, what args it needs
tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]

# 3. Ask a question AND hand over the tool menu
messages = [{"role": "user", "content": "What is 23 times 19?"}]
r = client.chat.completions.create(model="gemini-2.5-flash", messages=messages, tools=tools)
msg = r.choices[0].message

# 4. Did the model DECIDE to call a tool?
if msg.tool_calls:
    call = msg.tool_calls[0]
    args = json.loads(call.function.arguments)
    print("Model decided to call:", call.function.name, "with", args)

    # 5. YOUR code runs the real function
    result = multiply(args["a"], args["b"])
    print("Your code computed:", result)

    # 6. Feed the result back so the model can give a final answer
    messages.append(msg)
    messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
    final = client.chat.completions.create(model="gemini-2.5-flash", messages=messages, tools=tools)
    print("Final answer:", final.choices[0].message.content)
else:
    print("Model answered directly:", msg.content)