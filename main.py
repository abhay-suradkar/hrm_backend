from fastapi import FastAPI
from src.db_session.database import init_db
from src.auth.auth_api.auth_api import router as authAPI
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import firebase_admin
from firebase_admin import credentials

# Service Account JSON file path
cred = credentials.Certificate("firebase-private-key.json")

# Firebase Admin initialize karna (sirf ek baar)
firebase_admin.initialize_app(cred)

load_dotenv()
app =FastAPI()

init_db()

app.include_router(authAPI)

PORT = int(os.getenv("PORT", 13153))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)