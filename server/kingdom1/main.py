from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from passlib.hash import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATABASE_CONFIG = {
    "dbname": "royaldegen",
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "6575"
}


from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

# Utility function to connect to DB
def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

# Register Endpoint
@app.post("/register")
async def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    hashed_password = bcrypt.hash(user.password)
    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)
            """,
            (user.username, user.email, hashed_password)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        cursor.close()
        conn.close()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT * FROM users WHERE username = %s
        """,
        (user.username,)
    )
    db_user = cursor.fetchone()
    cursor.close()
    conn.close()
    if db_user and bcrypt.verify(user.password, db_user['password_hash']):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
class TextRequest(BaseModel):
    prompt: str
    temperature: float
    max_tokens: int

@app.post("/generate-text")
async def generate_text(request: TextRequest):
    try:
        headers = {
            "Authorization": "Bearer hf_ApiKey",
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
