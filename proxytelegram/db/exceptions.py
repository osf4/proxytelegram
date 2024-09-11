from proxytelegram.exceptions import ProxyTelegramException


class DBException(ProxyTelegramException):
    pass


class UserExists(DBException):
    pass


class UserNotFound(DBException):
    pass