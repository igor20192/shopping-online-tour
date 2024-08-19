import logging
from telethon import TelegramClient, events
import asyncio
from keywords_list import keywords
from decouple import config
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

api_id = config("API_ID")
api_hash = config("API_HASH")
phone_number = config("PHONE_NUMBER")
keyword = keywords
message_to_send = (
    "https://www.shoppingtour.click/catalogue/"  # Ссылка, которая будет отправлена
)
interval = 1800
similarity_threshold = 80  # Порог схожести (от 0 до 100)

client = TelegramClient("session_name", api_id, api_hash)


async def main():
    try:
        await client.start(phone=phone_number)
        logger.info("Клиент подключен")

        @client.on(events.NewMessage)
        async def handler(event):
            try:
                for keyword in keywords:
                    similarity = fuzz.partial_ratio(
                        keyword.lower(), event.raw_text.lower()
                    )
                    if similarity >= similarity_threshold:
                        logger.info(
                            f"Найдено ключевое слово в чате {event.chat_id}: {event.raw_text}"
                        )
                        chat_id = event.chat_id
                        await client.send_message(chat_id, message_to_send)
                        logger.info(f"Ссылка отправлена в чат {chat_id}")
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}")

        while True:
            try:
                async for dialog in client.iter_dialogs():

                    for keyword in keywords:
                        similarity = fuzz.partial_ratio(
                            keyword.lower(), dialog.name.lower()
                        )
                        if similarity >= similarity_threshold:
                            logger.info(f"Ключевое слово найдено в чате: {dialog.name}")
                            await client.send_message(dialog.id, message_to_send)
                            logger.info(f"Ссылка отправлена в чат {dialog.name}")
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                await asyncio.sleep(60)  # Ждем 1 минуту перед повторной попыткой

    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
    finally:
        await client.disconnect()
        logger.info("Клиент отключен")


with client:
    client.loop.run_until_complete(main())
