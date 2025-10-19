import requests
import json

def make_request_to_ollama(model_name:str, context:str, prompt:str):
    response = requests.post(url="http://localhost:11434/api/chat", json={
        "model": model_name,
        "message": [{
                "role":"user",
                "content": prompt
            },
            {
                "role":"system",
                "content":"context",

            }
        ],
        "streaming": False

    })
    
    print(response.json())
    return response.json()["message"]["content"]
