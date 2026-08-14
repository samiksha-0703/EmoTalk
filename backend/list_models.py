import requests
import os

API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

res = requests.get(url)
res.raise_for_status()

data = res.json()

for m in data.get("models", []):
    print(m["name"], "→", m.get("supportedGenerationMethods"))
