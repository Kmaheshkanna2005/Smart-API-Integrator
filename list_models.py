# list_grok_models.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("GROK_API_KEY"), base_url="https://api.x.ai/v1")

models = client.models.list()
for model in models.data:
    print(f"Model ID: {model.id}")