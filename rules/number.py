import re

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class IsNumberUser(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        if re.match(r'^[78]\d{10}$', event.text):
            return True
        else:
            await event.answer("Вы ввели не верный формат телефона. Попробуйте еще раз!")
            return False