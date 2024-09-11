from abc import ABC, abstractmethod
from proxytelegram.models.user import User


class BaseDB(ABC):
    """
    Abstract database for users
    """
    
    @abstractmethod
    async def create_user(self, user: User):
        """
        Create a user.

        Raise UserExists, if the user already exists
        """
        
        pass


    @abstractmethod
    async def get_user(self, id: int) -> User | None:
        """
        Return the user by his id.

        Return None, if there is no user with provided id
        """
        
        pass


    @abstractmethod
    async def get_user_by_topic_id(self, topic_id: int) -> User | None:
        """
        Return the user by topic id (message_thread_id).

        Return None, if there is no user with provided topic id
        """
        
        pass


    @abstractmethod
    async def delete_user(self, id: int):
        """
        Delete the user.

        Raise UserNotFound, if there is no user with provided id
        """
        
        pass


    @abstractmethod
    async def user_exists(self, id: int) -> bool:
        """
        Return True, if the user with provided id exists
        """
        
        pass


    @abstractmethod
    async def block_user(self, id: int):
        """
        Set True for 'blocked' property

        Raise UserNotFound, if there is no user with provided id
        """
        
        pass

    
    @abstractmethod
    async def unblock_user(self, id: int):
        """
        Set False for 'blocked' property

        Raise UserNotFound, if there is no user with provided id
        """

        pass


    @abstractmethod
    async def close(self):
        """
        Close all database connections
        """
        
        pass