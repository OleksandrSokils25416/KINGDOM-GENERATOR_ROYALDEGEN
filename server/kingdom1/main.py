from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gen_pipeline = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

class TextRequest(BaseModel):
    prompt: str

@app.post("/generate-text")
async def generate_text(request: TextRequest):
    try:
        output = gen_pipeline(request.prompt, max_length=300, do_sample=True, temperature=0.9)
        if output:
            return {"text": output[0]['generated_text']}
        else:
            raise HTTPException(status_code=500, detail="No text was generated.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
