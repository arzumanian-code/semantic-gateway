import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Semantic Gateway API")

# Получаем учетные данные из переменных окружения хостинга
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


class CandidateSubmission(BaseModel):
  name: str
  contact: str
  tech_stack: str
  motivation: str


@app.post("/submit-candidate")
def submit_candidate(data: CandidateSubmission):
  if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise HTTPException(
        status_code=500, detail="Telegram credentials are not configured on server."
    )

  # Формируем текст уведомления для вас
  message = (
      f"🎯 **Найден разработчик-энтузиаст!**\n\n"
      f"👤 **Имя:** {data.name}\n"
      f" коммуникация: {data.contact}\n"
      f"💻 **Стек/Опыт:** {data.tech_stack}\n"
      f"💡 **Мотивация / Ответ:** {data.motivation}"
  )

  telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "Markdown",
  }

  response = requests.post(telegram_url, json=payload)

  if response.status_code != 200:
    raise HTTPException(
        status_code=502, detail="Failed to send notification to Telegram."
    )

  return {
      "status": "success",
      "message": "Candidate verified and alert sent successfully.",
  }


@app.get("/")
def root():
  return {"status": "Gateway is active"}
