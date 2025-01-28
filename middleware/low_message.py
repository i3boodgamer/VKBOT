from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from database.engine import async_session


class MessageLowRegister(BaseMiddleware[Message]):
    def __init__(self, event, view):
        super().__init__(event, view)
        self.cached = False
    
    async def pre(self):
            self.event.text = self.event.text.lower()