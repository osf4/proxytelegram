import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from proxytelegram.bot.handlers import router
from proxytelegram.db.mongo import MongoDB
from proxytelegram.forwarder.supergroup import SupergroupForwarder
from proxytelegram.models.config import Config


async def main():
    config = Config()
    bot = Bot(config.bot.token)

    dp = Dispatcher(storage = MemoryStorage())
    dp.include_router(router)
    
    db = MongoDB(config.database.host, 
                 config.database.port, 
                 config.database.name)
    
    supergroup = config.bot.supergroup_id
    forwarder = SupergroupForwarder(bot, supergroup, db)

    await bot.delete_webhook()
    await dp.start_polling(bot,
                           config = config,
                           db = db,
                           forwarder = forwarder)
    
    await db.close()


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())