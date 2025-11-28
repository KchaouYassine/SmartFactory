import openai
import os

# create Groq client
def make_client(api_key=None, base_url=None):
    api_key = os.getenv("GROQ_API_KEY")
    return openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


