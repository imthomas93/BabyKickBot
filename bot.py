import logging
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from datetime import datetime, timedelta
import os

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Google Sheets Setup
SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/home/ec2-user/config.json'
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

gc = gspread.authorize(creds)
spreadsheet = gc.open("Baby Expenses")  # Replace with your Google Sheet name
sheet = spreadsheet.worksheet("Kicks Log")  # Replace "Kicks Log" with the exact sheet title

# Whitelist telegram users
ALLOWED_USERS = [ID_1, ID_2]  # restricted to Wife and me

# Define error handler
async def error_handler(update: Update, context: CallbackContext):
    try:
        raise context.error
    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Define restricted access decorator
def restricted(func):
    async def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context)
    return wrapper

@restricted
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome to Baby C movement logging! Use /kick to log a her kick and /summary to see today's kicks."
    )

@restricted
async def log_kick(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    timestamp = datetime.now()

    # Retrieve all data excluding the header
    records = sheet.get_all_values()[1:]  # Skip the header row

    # Filter records for this user
    user_kicks = [row for row in records if row[0] == str(user_id)]

    if user_kicks:
        # Get the timestamp of the last logged kick
        last_kick_time = datetime.strptime(user_kicks[-1][1], '%Y-%m-%d %H:%M:%S')

        # Check if the new kick is within 5 minutes of the last kick
        if timestamp - last_kick_time < timedelta(minutes=5):
            await update.message.reply_text(
                f"You can log kicks only after 5 minutes since the last one.\n"
                f"Baby's last kick was logged at {last_kick_time.strftime('%Y-%m-%d %H:%M:%S')}."
            )
            return

    # Log the kick to Google Sheets
    sheet.append_row([user_id, timestamp.strftime('%Y-%m-%d %H:%M:%S')])

    # Notify user
    await update.message.reply_text(f"Kick logged at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}!")

    # Retrieve all kicks from the last 12 hours
    twelve_hours_ago = timestamp - timedelta(hours=12)
    recent_kicks = [
        row for row in records if datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') > twelve_hours_ago and row[0] == str(user_id)
    ]

    # Check if the count reaches more than 10
    if len(recent_kicks) >= 10:
        # Prepare the summary
        response = f"Kicks in the last 12 hours: {len(recent_kicks)}\n"
        response += "\n".join(row[1] for row in recent_kicks)  # Show timestamp of each kick

        # Send the summary to the user
        await update.message.reply_text(
            f"Baby has more than 10 kicks in the last 12 hours. Here's the summary:\n{response}"
        )

@restricted
async def summary(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    # Retrieve all data excluding the header
    records = sheet.get_all_values()[1:]  # Skip the first row (header)

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Filter records for today
    kicks_today = [
        row for row in records
        if row[1].startswith(today)  # Assuming "kick timestamp" is in the second column
    ]

    if not kicks_today:
        await update.message.reply_text("No kicks recorded yet today!")
        return

    # Prepare the summary
    response = f"Kicks today: {len(kicks_today)}\n"
    response += "\n".join(row[1].split()[1] for row in kicks_today)  # Extract time from timestamp
    await update.message.reply_text(response)

def main():
    # Create the application object with your bot token
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("kick", log_kick))
    application.add_handler(CommandHandler("summary", summary))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start polling to receive updates
    application.run_polling()

if __name__ == "__main__":
    main()
