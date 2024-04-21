import requests
import os

API_URL = "https://x3oc0flj7a6sgv1j.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Authorization": f"Bearer {os.environ['HF_API_KEY']}"}

def query(input_text):
    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    prompt = "12 bar blues in C major with a swing feel."
    out = query(prompt)
    print(out)