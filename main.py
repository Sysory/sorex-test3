import asyncio
import logging
from os import environ
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from cryptoAPI import CryptoAPI
from handlers import router
from handlers import uman
from user import User

api = CryptoAPI(environ["API_KEY"])

async def checkingLoop(bot : Bot, delay = 30):
    while True:
        users : list[User] = uman.loadUsers()
        logging.info(f"{len(users)} users subscribed to updates")
        for user in users:
            currencies = user.userData.getAllCurrencies()

            logging.info("Updating prices...")
            prices = await api.loadActualData(currencies)
            logging.info("Updating prices... Done")
            await asyncio.sleep(0)

            for curr in currencies:
                id = curr.id.upper()
                if (float(prices[id]) <= float(curr.minVal)):
                    await bot.send_message(user.userData.userID, f"Валюта {id} достигла нижней границы! стоимость: {prices[id]}")

                if (float(prices[id]) >= float(curr.maxVal)):
                    await bot.send_message(user.userData.userID, f"Валюта {id} достигла верхней границы! стоимость: {prices[id]}")

        await asyncio.sleep(delay)

async def main():
    logging.info(f"--- Start session at {datetime.now()} ---")
    bot = Bot(token=environ["BOT_TOKEN"])
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    loop = asyncio.create_task(checkingLoop(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    file = open("log.txt", 'a')
    logging.basicConfig(level=logging.INFO, stream=file)
    asyncio.run(main())