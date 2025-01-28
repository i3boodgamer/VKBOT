from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from database.engine import async_session


class DataBaseSession(BaseMiddleware[Message]):
    def __init__(self, event, view):
        super().__init__(event, view)
        self.cached = False
    
    async def pre(self):
        async with async_session() as session:
            self.send({"session": session})