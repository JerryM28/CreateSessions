import asyncio
import os
import json
import logging
import time
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import socks
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Initialize logging
logger = logging.getLogger('telegram_sessions')
logger.setLevel(logging.INFO)

# Create a file handler which logs even debug messages
fh = logging.FileHandler('telegram_sessions.log')
fh.setLevel(logging.INFO)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create a formatter and set the formatter for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']

# Proxy settings
proxy = {
    'proxy_type': socks.HTTP, #sesuaikan jenis proxy default HTTP
    'addr': 'UrlProxy',
    'port': isiPORT,
    'username': 'usernameProxy',
    'password': 'passwordProxy'
}

# Device and app information
device_model = "Google Pixel 6"
system_version = "Android 12"
app_version = "10.15.1"
lang_code = "en"
system_lang_code = "en-US"

# Session folder
session_folder = "sessions"

async def check_sessions():
    start_time = time.time()  # Start timer
    session_files = [f for f in os.listdir(session_folder) if f.endswith('.session')]
    
    if not session_files:
        logger.warning("No session files found.")
        return

    total_sessions = len(session_files)
    active_sessions = 0
    inactive_sessions = 0

    for idx, session_file in enumerate(session_files, start=1):
        phone_number = session_file.replace('.session', '')
        session_path = os.path.join(session_folder, session_file)

        client = TelegramClient(
            session_path,
            api_id,
            api_hash,
            proxy=proxy,
            device_model=device_model,
            system_version=system_version,
            app_version=app_version,
            lang_code=lang_code,
            system_lang_code=system_lang_code
        )

        try:
            await client.connect()
            if await client.is_user_authorized():
                print(f"{Fore.WHITE}{idx}. Session for {phone_number} {Fore.GREEN}is active.{Style.RESET_ALL}")
                active_sessions += 1
            else:
                print(f"{Fore.WHITE}{idx}. Session for {phone_number} {Fore.RED}is not active.{Style.RESET_ALL}")
                inactive_sessions += 1
        except FloodWaitError as e:
            print(f"{Fore.YELLOW}{idx}. Rate limit exceeded for {phone_number}. Error: {str(e)}{Style.RESET_ALL}")
            logger.warning(f"Rate limit exceeded for {phone_number}: {e}")
        except Exception as e:
            print(f"{Fore.RED}{idx}. Error checking session for {phone_number}: {str(e)}{Style.RESET_ALL}")
            logger.error(f"Error checking session for {phone_number}: {e}")
        finally:
            await client.disconnect()
            await asyncio.sleep(2)  # Short delay between session checks

    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time

    # Log summary
    print(f"\nTotal execution time: {elapsed_time:.2f} seconds")
    print(f"Total sessions checked: {total_sessions}")
    print(f"Active sessions: {active_sessions}")
    print(f"Inactive sessions: {inactive_sessions}")

if __name__ == "__main__":
    asyncio.run(check_sessions())