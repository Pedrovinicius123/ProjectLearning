import requests
import json
import os
from dotenv import load_dotenv
from ollama import Client



load_dotenv()
API_KEY = os.getenv("OLLAMA_API_KEY")

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_API_KEY')}
)
base_url = "http://localhost:11434/api/generate"

def make_request_to_ollama_reasoning(model_name:str, context:str, prompt:str, n_tokens:int, use_cloud=False):
    response = None
    if use_cloud:
        response = client.chat(model_name, messages=[{
                "role":"user",
                "content": prompt
            },
            {
                "role":"system",
                "content":context,

            }
        ], options={
            "num_predict":n_tokens,
            "temperature": 0.2,

        }, stream=False, think=True)

        return response["message"]["content"]

    else:
        response = requests.post(base_url, json={
            "model":model_name,
            "prompt": f"CONTEXTO ANTERIOR: {context}\n\n PROMPT: {prompt}",
            "options": {
                "num_predict": n_tokens,
                "temperature": 0

            },
            "streamming":False
        })


        return response.json()["response"]

def make_request_to_ollama_compile(model_name:str, context:str, n_tokens:int, use_cloud=False):
    response = None
    if use_cloud:
        response = client.chat(model_name, messages=[{
                "role":"user",
                "content": "Compile tudo em um só relatório rigoroso, citando artigos e o Ollama"
            },
            {
                "role":"system",
                "content":context,

            }
        ], options={
            "num_predict":n_tokens,
            "temperature": 0.2,

        }, stream=False, think=True)

        return response["message"]["content"]

    else:
        response = requests.post(base_url, json={
            "model":model_name,
            "prompt": f"CONTEXTO ANTERIOR: {context}\n\n PROMPT: Compile tudo em um só relatório rigoroso, citando artigos e o Ollama",
            "options": {
                "num_predict": n_tokens,
                "temperature": 0

            },
            "streamming":False
        })

        return response.json()["response"]
