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
# IMPORTANT: For Render, you should ideally use environment variables for keys,
# not embed a JSON file directly in your repo.
# If 'firebase-private-key.json' is sensitive, consider passing its content
# as an environment variable or ensure it's handled securely by Render's secrets management.
cred = credentials.Certificate("firebase-private-key.json")

# Firebase Admin initialize karna (sirf ek baar)
firebase_admin.initialize_app(cred)

load_dotenv()
app = FastAPI()

init_db()

app.include_router(authAPI)

# You don't need to explicitly set PORT here for Render deployment.
# Render will provide it via the $PORT environment variable to Uvicorn.
# PORT = int(os.getenv("PORT", 13153)) # This line is not strictly needed for Render

# --- REMOVE OR COMMENT OUT THIS BLOCK FOR DEPLOYMENT ON RENDER ---
# This block is for local development only.
# Render's start command (uvicorn src.main:app --host 0.0.0.0 --port $PORT)
# handles running Uvicorn and binding to the correct port.
# if __name__ == "__main__":
#     import uvicorn
#     # Using reload=True is also generally not recommended for production.
#     uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)
# ------------------------------------------------------------------