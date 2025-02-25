import requests
import json
import os
import random
from datetime import datetime

# 🔹 Replace these with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7523061594:AAFxrIIaLGMEw_49YUS5XOb_KG-sSW-zzAM"
CHAT_ID = "7441746164"

# 🔹 File to store previous questions
QUESTIONS_FILE = "questions.json"

# 🔹 Replace with your extracted cookies
COOKIES = {
    "hackerrank_mixpanel_token": "2dab64b2-51e9-4c69-a1da-0014edcf9825",
    "peacemakers24b1_crp": "*nil*",
    "session_id": "0yhigm53-1740482754625",
    "user_type": "hacker",
    "_hrank_session": "ebfd03a3d3d948fd372abfe176cbb7f2",
}

# 🔹 Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

# 🔹 Contest Slug
CONTEST_SLUG = "peacemakers24b1"

# 🔹 Motivational & Engaging Messages
NEW_QUESTION_MESSAGES = [
    "🚀 A new challenge has arrived! Time to sharpen your mind and break some limits. 💡",
    "⚔️ A fresh coding battle awaits! Will you emerge victorious? The challenge is yours! 🔥",
    "💡 The path to greatness is built one problem at a time. A new challenge is here—conquer it! 🔥",
    "📜 Another step on your coding journey unfolds. Will you take on the challenge? 💪",
    "🌟 A new problem stands before you. Solve it, and take one step closer to mastery! 🏆",
    "🔥 Champions rise with every challenge they conquer. A new one just dropped—go claim victory! 🏅",
    "💻 New question alert! Time to turn logic into magic. Can you solve it? 🚀",
    "🎯 Focus, code, conquer! A new problem just arrived—show it who’s boss. 💪",
    "🧠 A new challenge has appeared on your journey. Accept it, and grow stronger! 🌱",
]

NO_NEW_QUESTION_MESSAGES = [
    "⏳ No new questions today, but that’s no excuse to stop growing. Keep sharpening your skills! ⚡",
    "📖 Even legends have days of rest. No new problems today—use this time to level up! 💡",
    "🌙 No new challenges tonight, but the real challenge? Staying consistent. Keep coding! 💻",
    "🚀 No new questions today, but preparation is key. Keep your mind sharp for tomorrow! ⚡",
    "🔥 No challenges today, but champions train even in silence. Use today wisely! 🏆",
    "🏋️ No new problems, but that doesn’t mean you can’t practice! Stay ready for the next challenge. 💪",
    "🎯 A day without a question is a chance to refine your strengths. Keep pushing forward! 🔥",
    "📅 No new problems today, but every coder knows: Growth happens daily. Keep at it! 💡",
    "⏸️ No new challenges uploaded yet, but patience is a part of mastery. Keep improving! 🏅",
]

# 🔹 Function to send a Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    return response.json()

# 🔹 Function to load previously stored questions
def load_previous_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as file:
            return json.load(file)
    return []

# 🔹 Function to save new questions
def save_questions(questions):
    with open(QUESTIONS_FILE, "w") as file:
        json.dump(questions, file, indent=4)

# 🔹 Fetch Questions from HackerRank
def fetch_questions():
    offset = 0
    limit = 10
    all_questions = []

    while True:
        url = f"https://www.hackerrank.com/rest/contests/{CONTEST_SLUG}/challenges?offset={offset}&limit={limit}&track_login=true"
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        
        if response.status_code == 200:
            data = response.json()
            questions = data.get("models", [])

            if not questions:  # No more questions left
                break

            for question in questions:
                all_questions.append(question["name"])

            offset += limit  # Move to the next batch

        else:
            print(f"❌ Request Failed! Status Code: {response.status_code}")
            return []

    return all_questions

# 🔹 Check for new questions and notify on Telegram
def check_for_new_questions():
    previous_questions = load_previous_questions()
    current_questions = fetch_questions()

    new_questions = [q for q in current_questions if q not in previous_questions]

    if new_questions:
        message = random.choice(NEW_QUESTION_MESSAGES) + "\n\n" + "\n".join([f"🔹 {q}" for q in new_questions])
        send_telegram_message(message)
        save_questions(current_questions)
        print("✅ New questions sent to Telegram!")
    else:
        current_hour = datetime.now().hour
        if current_hour >= 23:  # If it's after 11 PM
            message = random.choice(NO_NEW_QUESTION_MESSAGES)
            send_telegram_message(message)
            print("⚡ No new questions. Sent a motivational message!")

# 🔹 Run the script
check_for_new_questions()
send_telegram_message("🚀 Testing direct message from script!")






