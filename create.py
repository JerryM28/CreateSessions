import asyncio
import os
import json
import logging
from colorama import init, Fore
from logging.handlers import RotatingFileHandler
import socks
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

init(autoreset=True)

# Set up logging
logger = logging.getLogger('telegram_sessions')
logger.setLevel(logging.INFO)

# Create a file handler which logs even debug messages
fh = RotatingFileHandler('telegram_sessions.log', maxBytes=1000000, backupCount=3)
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
two_step_password = 'ISI_password_kalo_pake' 

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

# Ensure session folder exists
session_folder = "sessions"
os.makedirs(session_folder, exist_ok=True)

def get_phone_numbers():
    try:
        with open('number.txt', 'r') as file:
            numbers = [line.strip() for line in file if line.strip()]
            if numbers:
                logger.info(f"{len(numbers)} phone numbers found in number.txt.")
                return numbers
            else:
                logger.warning("number.txt is empty.")
    except FileNotFoundError:
        logger.warning("number.txt not found.")
    return []

async def create_sessions(phone_numbers, create=True):
    if not phone_numbers:
        logger.error("No phone numbers to process.")
        return

    if create:
        for idx, phone_number in enumerate(phone_numbers):
            session_file = f'{phone_number}.session'
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
                logger.info(f"Creating session for phone number: {phone_number}")
                await client.connect()

                if not await client.is_user_authorized():
                    await client.send_code_request(phone_number)
                    logger.info("OTP code sent.")
                    
                    while True:
                        code = input("Enter OTP code: ")
                        try:
                            await client.sign_in(phone_number, code)
                            break
                        except SessionPasswordNeededError:
                            logger.info("Password required after OTP...")
                            await client.sign_in(password=two_step_password)
                            logger.info("Password accepted, login successful!")
                            break
                        except Exception as e:
                            logger.error(f"Invalid OTP. Please try again. Error: {str(e)}")
                            continue

                    if await client.is_user_authorized():
                        logger.info(f"Session created and login successful for {phone_number}!")
                    else:
                        logger.error(f"Login failed for {phone_number}.")
                else:
                    logger.info(f"Session already exists for {phone_number}.")
            except Exception as e:
                logger.error(f"Error creating session for {phone_number}: {str(e)}")
            finally:
                await client.disconnect()
                await asyncio.sleep(5)  # Delay between accounts
    else:
        for idx, phone_number in enumerate(phone_numbers):
            logger.info(f"{idx + 1}. {phone_number}")
        session_idx = int(input(Fore.CYAN + "Select phone number to create session: ")) - 1
        if session_idx < 0 or session_idx >= len(phone_numbers):
            logger.error("Invalid phone number selection.")
            return

        phone_number = phone_numbers[session_idx]
        session_file = f'{phone_number}.session'
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
            logger.info(f"Creating session for phone number: {phone_number}")
            await client.connect()

            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                logger.info("OTP code sent.")

                while True:
                    code = input("Enter OTP code: ")
                    try:
                        await client.sign_in(phone_number, code)
                        break
                    except SessionPasswordNeededError:
                        logger.info("Password required after OTP...")
                        await client.sign_in(password=two_step_password)
                        logger.info("Password accepted, login successful!")
                        break
                    except Exception as e:
                        logger.error(f"Invalid OTP. Please try again. Error: {str(e)}")
                        continue

                if await client.is_user_authorized():
                    logger.info(f"Session created and login successful for {phone_number}!")
                else:
                    logger.error(f"Login failed for {phone_number}.")
            else:
                logger.info(f"Session already exists for {phone_number}.")
        except Exception as e:
            logger.error(f"Error creating session for {phone_number}: {str(e)}")
        finally:
            await client.disconnect()
            await asyncio.sleep(5)  # Delay between accounts

# Main entry point
def main():
    # Welcome message
    print(Fore.GREEN + "Welcome to the Telegram Session Creator!")
    print("This script will help you create and manage Telegram sessions.")
    print("Please ensure that you have your phone numbers listed in number.txt.")
    
    # Menu options
    print(Fore.YELLOW + "Select an option:")
    print("1. Create sessions for all phone numbers")
    print("2. Select a phone number to create session")
    
    option = input(Fore.CYAN + "Enter your choice (1 or 2): ")

    if option == '1':
        phone_numbers = get_phone_numbers()
        asyncio.run(create_sessions(phone_numbers, create=True))
    elif option == '2':
        phone_numbers = get_phone_numbers()
        asyncio.run(create_sessions(phone_numbers, create=False))
    else:
        logger.error("Invalid option selected.")

if __name__ == "__main__":
    main()
