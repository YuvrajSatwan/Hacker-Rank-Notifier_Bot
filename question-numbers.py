import requests
import os
import datetime

# Replace with your Telegram bot API token and chat ID
TELEGRAM_BOT_TOKEN = "7211810846:AAFchPh2P70ZWlQPEH1WAVgaLxngvkHmz3A"
TELEGRAM_CHAT_ID = "1631288026"

# File to store the last question count and last update time
COUNT_FILE = "question_count.txt"
LAST_UPDATE_FILE = "last_update.txt"

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
    """Fetch all questions from the contest and return their names."""
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
                all_questions.append(question["name"])  # Store question names

            offset += limit  # Move to the next batch

        else:
            print(f"❌ Request Failed! Status Code: {response.status_code}")
            return None, []  # Return None for count and an empty list

    return len(all_questions), all_questions  # Return both count and names

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

    # Save last update time
    with open(LAST_UPDATE_FILE, "w") as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%d"))

def get_last_update_date():
    """Read the last update date from file."""
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, "r") as file:
            return file.read().strip()
    return None

def notify_question_count():
    """Fetch, compare, and send question count update with names to Telegram."""
    question_count, question_names = fetch_questions()

    if question_count is None:
        print("❌ Failed to fetch questions.")
        return

    last_count = get_last_count()

    if last_count is None:
        message = f"🚀 First Check! {question_count} questions are live!\n\n📌 **Latest Questions:**\n" + "\n".join([f"🔹 {q}" for q in question_names])
    else:
        difference = question_count - last_count
        if difference > 0:
            new_questions = question_names[-difference:]  # Get only newly added questions

            messages = [
    f"🔥 {difference} new coding challenges just arrived! Will you be the first to solve them? ⚡",
    f"💡 BOOM! {difference} fresh problems are waiting for you. Time to showcase your skills! 🚀",
    f"⚔️ A new war begins! {difference} more puzzles to crack. Are you the coding champion? 👑",
    f"🤖 {difference} fresh problems have dropped! Will you rise or fall? The battle is on! 🔥",
    f"⏳ Time waits for none! {difference} new questions are here. Ready to claim your rank? 🏆",
    f"🚀 *A new era begins...* {difference} fresh challenges have arrived. Will you rise to the occasion? ⚔️🔥",
    f"🧠 *The battle of minds ignites!* {difference} new problems await. Who will claim victory? 🏆",
    f"⚡ *Anomaly detected!* {difference} new coding puzzles have surfaced. Time to decode the unknown! 🤖",
    f"🌌 *The void shifts...* {difference} challenges have emerged. Only the worthy will conquer them! ⚔️",
    f"🛡️ *A warrior’s path is never easy!* {difference} new trials have been unleashed. Face them with courage! 💡",
    f"⏳ *Time waits for no one!* {difference} more problems stand between you and greatness. Will you take them on? 🏅",
    f"📜 *A new scroll has been uncovered!* The secrets within these {difference} questions are waiting for a true solver! 🔍",
    f"💥 *The battlefield roars!* {difference} new coding quests have arrived. Show the world your skills! 🌟",
    f"🤖 *AI detects new challenges...* {difference} coding mysteries await. Will you solve them before anyone else? ⚙️",
    f"🕵️ *A secret has been unveiled...* {difference} fresh problems are here. The hunt for solutions begins now! 🔥"
]

message = messages[difference % len(messages)]  # Randomized message selection

            
            base_message = messages[difference % len(messages)]  # Randomized message
            question_list = "\n".join([f"🔹 {q}" for q in new_questions])  # Format question names
            message = f"{base_message}\n\n📌 **New Questions:**\n{question_list}"
        else:
            print("No new questions. Skipping notification.")
            return

    send_telegram_message(message)
    save_new_count(question_count)



def check_end_of_day():
    """Send a message if no new questions were uploaded by 11 PM IST."""
    current_time = datetime.datetime.now()
    
    # Convert to IST (UTC +5:30)
    ist_time = current_time + datetime.timedelta(hours=5, minutes=30)
    
    if ist_time.hour == 22 and ist_time.minute == 40:  # 10:40 PM IST

        last_update_date = get_last_update_date()
        today_date = ist_time.strftime("%Y-%m-%d")

        if last_update_date != today_date:  # No update today
            messages = [
                "🕰️ The battlefield remained quiet today. But remember, the real warriors sharpen their blades in silence. ⚔️🔥",
                "🤖 No new challenges today, but legends never rest. Stay sharp, for the storm may arrive tomorrow! ⚡",
                "⏳ A day without new battles... The silence before the storm? Stay alert, coder! 🚀",
                "🌓 The coding universe is silent tonight. Perhaps a challenge awaits at dawn? Be ready! 🌅",
                "💭 No new puzzles today, but every great coder knows – the best battles are fought in the mind first. Keep practicing! 🏆"
            ]
            message = messages[ist_time.day % len(messages)]  # Random message
            send_telegram_message(message)

# Run the function
notify_question_count()
check_end_of_day()
