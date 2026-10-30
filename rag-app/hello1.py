from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain RAG in 2 sentences."}],
)

print(response.choices[0].message.content)
