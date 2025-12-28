# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conversation.session import LeadQualifierSession

app = FastAPI()

# CORS for frontend demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = LeadQualifierSession(debug=True)

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    return bot.process_message(req.message)


@app.post("/reset")
def reset():
    global bot
    bot = LeadQualifierSession(debug=True)
    return {"status": "reset"}
