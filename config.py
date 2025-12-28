# config.py

# 🔐 API Keys
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 this loads .env into environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")



# 🤖 Model config
MODEL_NAME = "llama-3.3-70b-versatile"

# 🎛️ Generation controls
TEMPERATURE = 0.2
MAX_TOKENS = 512
