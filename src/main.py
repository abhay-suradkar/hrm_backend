from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db_session.database import init_db
from src.auth.auth_api.auth_api import router as authAPI
import os
from dotenv import load_dotenv
import sys
import firebase_admin
from firebase_admin import credentials

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

cred = credentials.Certificate("firebase-private-key.json")
firebase_admin.initialize_app(cred)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(authAPI)
