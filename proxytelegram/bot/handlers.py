from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from proxytelegram.db.base import BaseDB
from proxytelegram.forwarder.base import BaseForwarder
from proxytelegram.models.config import Config

from .commands import BotCommands


router = Router(name = __name__)


@router.message(CommandStart())
async def handle_start(msg: Message, config: Config):
    if config.bot.greeting_message:
        await msg.answer(config.bot.greeting_message)


@router.message(Command(BotCommands.block, BotCommands.unblock))
async def handle_block(msg: Message, command: CommandObject, db: BaseDB):
    if not _message_from_admin(msg):
        return 
    
    user = await db.get_user_by_topic_id(msg.message_thread_id)
    if not user:
        return

    blocked = command.command == BotCommands.block
    await _block_or_unblock_user(db, user.id, blocked)

    await msg.answer(f'The user was {'blocked' if blocked else 'unblocked'}')


@router.message()
async def handle_new_message(msg: Message, forwarder: BaseForwarder, config: Config):
    if not _message_from_admin(msg):
        await forwarder.forward_message(msg)

    else:
        if not _message_from_bot(msg, config):
            # bot handles his own messages like from the others
            await forwarder.answer_message(msg)


async def _block_or_unblock_user(db: BaseDB, user_id: str, block: bool):
    if block:
        await db.block_user(user_id)

    else:
        await db.unblock_user(user_id)


def _message_from_admin(msg: Message) -> bool:
    """
    Return True, if the message was sent by the admin.

    Only the bot and the admin are able to send messages to the supergroup,
    so every message with message_thread_id != None are determined as from the admin
    """
    
    return not msg.message_thread_id is None


def _message_from_bot(msg: Message, config: Config) -> bool:
    return msg.from_user.username == config.bot.username