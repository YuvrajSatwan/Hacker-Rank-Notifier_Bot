import requests
import os

# Replace with your Telegram bot API token and chat ID
TELEGRAM_BOT_TOKEN = "7211810846:AAFchPh2P70ZWlQPEH1WAVgaLxngvkHmz3A"
TELEGRAM_CHAT_ID = "1631288026"

# File to store the last question count
COUNT_FILE = "question_count.txt"

# Replace the cookies below with your extracted cookies
COOKIES = {
    "hackerrank_mixpanel_token": "2dab64b2-51e9-4c69-a1da-0014edcf9825",
    "peacemakers24b1_crp": "*nil*",
    "session_id": "0yhigm53-1740482754625",
    "user_type": "hacker",
    "_hrank_session": "ebfd03a3d3d948fd372abfe176cbb7f2",
}

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

# Contest Slug (Change if needed)
CONTEST_SLUG = "peacemakers24b1"


def fetch_questions():
    """Fetch all questions from the contest."""
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
            return None  # Return None if request fails

    return len(all_questions)


def send_telegram_message(message):
    """Send a Telegram message notification."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("✅ Telegram notification sent!")
    else:
        print("❌ Failed to send Telegram notification.")


def get_last_count():
    """Read the last stored question count from the file."""
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return None  # Handle corrupt or empty file
    return None  # Return None if file doesn't exist


def save_new_count(count):
    """Save the latest question count to the file."""
    with open(COUNT_FILE, "w") as file:
        file.write(str(count))


def notify_question_count():
    """Fetch, compare, and send question count update to Telegram."""
    question_count = fetch_questions()

    if question_count is None:
        print("❌ Failed to fetch questions.")
        return

    last_count = get_last_count()

    if last_count is None:
        message = f"📢 First Run! Total Questions in {CONTEST_SLUG}: {question_count}"
    else:
        difference = question_count - last_count
        if difference > 0:
            message = f"📢 New Questions Added! 📈\nTotal: {question_count} (⬆️ +{difference})"
        else:
            message = f"📢 Total Questions in {CONTEST_SLUG}: {question_count} (No Change)"

    send_telegram_message(message)
    save_new_count(question_count)


# Run the function
notify_question_count()
