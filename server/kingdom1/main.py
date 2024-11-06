from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    prompt: str
    temperature: float
    max_tokens: int

@app.post("/generate-text")
async def generate_text(request: TextRequest):
    try:
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": request.prompt,
            "parameters": {
                "temperature": request.temperature,
                "max_new_tokens": request.max_tokens,
            },
        }
        response = requests.post("https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct", headers=headers, json=payload)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="API call failed")

        generated_text = response.json()[0]["generated_text"]
        return {"text": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")
