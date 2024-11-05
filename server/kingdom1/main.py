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

# Define the text-generation pipeline using a free model
text_generator = pipeline("text-generation", model="gpt2")  # Or another model like 'distilgpt2'

class TextRequest(BaseModel):
    prompt: str


def format_prompt(key_phrases: str) -> str:
    return (
        f"Generate a story and name for a kingdom based on the following descriptions: {key_phrases}. "
        "Describe the kingdom's name, story, and landscape, and create an engaging medieval narrative."
    )


@app.post("/generate-text")
async def generate_text(request: TextRequest):
    try:
        formatted_prompt = format_prompt(request.prompt)

        # Use the text generator pipeline to get a response
        generated_text = text_generator(formatted_prompt, max_length=500, num_return_sequences=1)[0]["generated_text"]
        return {"text": generated_text}

    except Exception as e:
        print("Error:", e)  # Logs the error details
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")
