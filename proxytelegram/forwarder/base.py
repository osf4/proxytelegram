from abc import ABC, abstractmethod
from aiogram.types import Message


class BaseForwarder(ABC):
    """
    Forwarder allows to send messages between the admin and users
    """

    @abstractmethod
    async def forward_message(self, msg: Message):
        """
        Forward the message from the user to the admin
        """
        
        pass


    @abstractmethod
    async def answer_message(self, message_id: int, msg: Message):
        """
        Forward the message from the admin to the user
        """
        
        pass