import logging
from telethon import TelegramClient, events
import asyncio
from keywords_list import keywords
from decouple import config
from fuzzywuzzy import fuzz

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Fetching API data and phone number from environment variables
api_id = config("API_ID")
api_hash = config("API_HASH")
phone_number = config("PHONE_NUMBER")

# List of keywords and the message to be sent
message_to_send = "https://www.shoppingtour.click/catalogue/"
interval = int(
    config("INTERVAL", default=1800)
)  # Interval for sending messages in seconds
similarity_threshold = int(
    config("SIMILARITY_THRESHOLD", default=80)
)  # Similarity threshold (from 0 to 100)

# Telegram client initialization
client = TelegramClient("session_name", api_id, api_hash)


async def send_message_to_chat(chat_id, message):
    """
    Sends a message to a specified chat.

    :param chat_id: The ID of the chat to send the message to.
    :param message: The message to be sent.
    """
    try:
        await client.send_message(chat_id, message)
        logger.info(f"Message sent to chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send message to chat {chat_id}: {e}")


async def process_new_message(event):
    """
    Processes new incoming messages and checks for keyword matches.

    :param event: Event of a new message in the chat.
    """
    try:
        for keyword in keywords:
            similarity = fuzz.partial_ratio(keyword.lower(), event.raw_text.lower())
            if similarity >= similarity_threshold:
                logger.info(
                    f"Keyword found in message {event.chat_id}: {event.raw_text}"
                )
                await send_message_to_chat(event.chat_id, message_to_send)
                break  # Stop after the first match
    except Exception as e:
        logger.error(f"Error processing message: {e}")


async def process_dialogs():
    """
    Iterates through all dialogs and checks for keyword matches in chat names and messages.
    """
    try:
        async for dialog in client.iter_dialogs():
            for keyword in keywords:
                similarity = fuzz.partial_ratio(keyword.lower(), dialog.name.lower())
                if similarity >= similarity_threshold:
                    logger.info(f"Keyword found in chat: {dialog.name}")
                    await send_message_to_chat(dialog.id, message_to_send)
                    break  # Stop after the first match

    except Exception as e:
        logger.error(f"Error processing dialogs: {e}")


async def main():
    """
    Main function that starts the Telegram client and sets up event handlers.
    """
    try:
        await client.start(phone=phone_number)
        logger.info("Client connected")

        # Event handler for new messages
        @client.on(events.NewMessage)
        async def handler(event):
            await process_new_message(event)

        while True:
            await process_dialogs()
            await asyncio.sleep(interval)
    except Exception as e:
        logger.critical(f"Critical error: {e}")
    finally:
        await client.disconnect()
        logger.info("Client disconnected")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
