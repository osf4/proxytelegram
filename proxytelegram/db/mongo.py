from motor.motor_asyncio import AsyncIOMotorClient
from proxytelegram.models.user import User

from .base import BaseDB
from .exceptions import UserExists, UserNotFound


class MongoDB(BaseDB):
    """
    User database based on MongoDB
    """
    
    def __init__(self, host: str, port: str, database: str):
        self.host = host
        self.port = port

        self.database = database

        self.__client = AsyncIOMotorClient(host, port)
        self.__database = self.__client[database]

        self.__users = self.__database['users']

    
    async def create_user(self, user: User):
        if await self.user_exists(user.id):
            raise UserExists(f'User with ID {user.id} already exists')
        
        await self.__users.insert_one(user.model_dump())


    async def get_user(self, id: int) -> User | None:
        raw = await self.__users.find_one({'id': id})

        return User.model_validate(raw) if raw else None
    

    async def get_user_by_topic_id(self, topic_id: int) -> User | None:
        raw = await self.__users.find_one({'topic_id': topic_id})

        return User.model_validate(raw) if raw else None
    

    async def delete_user(self, id: int):
        if not await self.user_exists(id):
            raise UserNotFound(f'User with ID {id} was not found')
        
        await self.__users.delete_one({'id': id})


    async def user_exists(self, id: int) -> bool:
        count = await self.__users.count_documents({'id': id})
        return count != 0


    async def block_user(self, id: int):
        await self.__update_blocked(id, True)
       

    async def unblock_user(self, id: int):
        await self.__update_blocked(id, False)


    async def close(self):
        self.__client.close()


    async def __update_blocked(self, id: int, blocked: bool):
        if not await self.user_exists(id):
            raise UserNotFound(f'User with ID {id} was not found')
        
        await self.__users.update_one({'id': id}, 
                                      {'$set': {'blocked': blocked}})