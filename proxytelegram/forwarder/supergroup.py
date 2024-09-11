from aiogram import Bot
from aiogram.types import Message

from proxytelegram.db.base import BaseDB
from proxytelegram.models.config import Config
from proxytelegram.models.user import User
from .base import BaseForwarder


class SupergroupForwarder(BaseForwarder):
    """
    SupergroupForwarder sends all messages from users into a supergroup.

    The forwarder creates a new topic for every new user.
    If the user writes a message, the forwarder sends it to that topic.
    If the admin writes a message to that topic, the forwarder sends it to the user
    """
    
    def __init__(self, 
                 bot: Bot, 
                 supergroup: str,
                 db: BaseDB):
        
        self.bot = bot

        self.supergroup = supergroup
        self.db = db


    async def forward_message(self, msg: Message):
        user = await self.db.get_user(msg.from_user.id)
        if not user:
            user = await self.__create_user(msg)
        
        if not user.blocked:
            await msg.forward(self.supergroup,
                              message_thread_id = user.topic_id)


    async def answer_message(self, msg: Message):
        user = await self.db.get_user_by_topic_id(msg.message_thread_id)
        if user:
            await msg.copy_to(user.id)


    async def __create_user(self, msg: Message) -> User:
        user = msg.from_user
        topic_name = f'{user.first_name} {user.id} {user.username}'

        topic_id = await self.__create_topic_for_user(topic_name)
        new_user = User(
            id = msg.from_user.id,
            topic_id = topic_id,
        )

        await self.db.create_user(new_user)
        return new_user
    
    async def __create_topic_for_user(self, name: str) -> int:
        topic = await self.bot.create_forum_topic(
            self.supergroup,
            name,
        )

        return topic.message_thread_id