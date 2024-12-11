import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import JWTError, jwt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Config
DATABASE_CONFIG = {
    "dbname": "royaldegen",
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "6575"
}

# JWT Secret and Algorithm
SECRET_KEY = "896d2416a271d7bab690ca7adb711a390b1e4e1ac6966a55412fc7b925f4d462477d6928713747c10b94efa17daef4e3543550b197685e9fc9a7f34873d03142710e1dfa97c5ab89bbed812fba4bba21d5093966f784f6e0c01a5210d78727e8c286a7f1d3f228a1fa4bd3df52bafe9a6204c7267f8f5d663b77a71f7aa85734252eb667e0b124c735a048710dd525bd063f58011c1653a1e08d8615b4210c06cdfbf281648a8cbdcb988a93244a254c21df1818206bd881f3bd976b4afe03e2964cee1f073f1a84517748ae3b0626db27f1e1f7436478dd5ee3d1f691c0577908563aa347aa5e398d8e1e606821bc2359d2b1c2fd0c4747f4fe1f59a5897bdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT helper functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        return username
    except JWTError as e:
        logging.error(f"JWT verification error: {str(e)}")
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def get_db_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Models
class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TextRequest(BaseModel):
    prompt: str
    temperature: float
    max_tokens: int

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
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        logging.error(f"Unique violation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception as e:
        conn.rollback()
        logging.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during registration")
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
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        logging.error(f"Failed login attempt for username: {user.username}")
        raise HTTPException(status_code=400, detail="Invalid username or password")

@app.post("/generate-text")
async def generate_text(request: TextRequest, authorization: Optional[str] = Header(None)):
    try:
        # Check if the authorization header is provided for JWT
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            try:
                username = verify_token(token)  # Verify JWT and extract username
            except HTTPException as e:
                logging.error(f"Token verification error: {str(e)}")
                raise HTTPException(status_code=403, detail="Invalid or expired token")
        else:
            username = None  # No authentication provided

        # Interpret the prompt as a list of tags
        tags = [tag.strip() for tag in request.prompt.split(",")]
        logging.debug(f"Extracted tags: {tags}")

        # Create a structured story based on the tags
        story_prompt = (
            "Create a kingdom story using the following elements: "
            + ", ".join(tags) +
            ". Include characters, events, and descriptions to bring the tags to life."
        )
        logging.debug(f"Generated story prompt: {story_prompt}")

        # Hugging Face API call
        headers = {"Authorization": f'Bearer {os.getenv("HF_APIKEY")}', "Content-Type": "application/json"}
        payload = {
            "inputs": story_prompt,
            "parameters": {"temperature": request.temperature, "max_new_tokens": request.max_tokens},
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
            headers=headers,
            json=payload,
            timeout=10
        )

        # Handle errors from Hugging Face API
        if response.status_code != 200:
            logging.error(f"Hugging Face API returned {response.status_code}: {response.text}")
            raise HTTPException(status_code=500, detail="API call failed")

        # Process the generated text
        full_text = response.json()[0]["generated_text"]
        logging.debug(f"Full text received: {full_text}")

        # Remove the root prompt text from the response
        cleaned_text = full_text.replace(story_prompt, "").strip()
        logging.info(f"Cleaned generated text: {cleaned_text}")

        # Save generated story if user is logged in
        if username:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()["id"]
            cursor.execute(
                """
                INSERT INTO prompts (user_id, prompt, temperature, max_tokens, generated_text)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, request.prompt, request.temperature, request.max_tokens, cleaned_text)
            )
            conn.commit()
            cursor.close()
            conn.close()

        # Check for NSFW content
        nsfw_directory = os.path.join(os.path.dirname(__file__), 'NSFW')
        nsfw_words_set = load_nsfw_words(nsfw_directory)
        isclear = check_text_for_nsfw_words(cleaned_text, nsfw_words_set)

        if not isclear:
            cleaned_text = "NSFW detected. Please try another prompt."

        return {"text": cleaned_text}

    except HTTPException as e:
        logging.error(f"HTTPException in /generate-text: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error in /generate-text: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def load_nsfw_words(directory):
    nsfw_words = set()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, encoding='utf-8') as file:
                for line in file:
                    nsfw_words.add(line.strip().lower())
    return nsfw_words

def check_text_for_nsfw_words(text, nsfw_words):
    words = text.lower().split()
    for word in words:
        if word in nsfw_words:
            return False
    return True
