from conversation.session import LeadQualifierSession

bot = LeadQualifierSession(debug=True)

messages = [
    "Looking for wedding photographer in Pune",
    "Wedding",
    "20th Feb",
    "Pune"
]

for msg in messages:
    print(f"\nUSER: {msg}")
    response = bot.process_message(msg)
    print("BOT:", response)
