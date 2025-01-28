import logging
import re

from vkbottle import Bot, API, CtxStorage, GroupEventType
from vkbottle.bot import Message, MessageEvent
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.session import DataBaseSession
from middleware.low_message import MessageLowRegister
from core.config import settings
from database.querys import (
    get_user_table,
    add_user_table,
    get_user_table_promocode,
    add_user_table_promocode,
    add_number,
    mute_bot,
    unmute_bot,
    is_mute_bot,
    get_user_number,
)
from utils.states import SuperStates


logging.getLogger("vkbottle").setLevel(logging.INFO)


api = API(settings.bot.TOKEN)
bot = Bot(api=api)

ctx = CtxStorage()




@bot.on.message(text="+")
async def answer(message: Message, session: AsyncSession):
    name_users = (await bot.api.users.get(user_ids=message.from_id))[0].first_name
    
    if await get_user_table(session=session, user_id=message.from_id) is None:
        await add_user_table(session=session, user_id=message.from_id, name=name_users)
        
    if await get_user_table_promocode(session=session, user_id=message.from_id) is None:
        await add_user_table_promocode(session=session, user_id=message.from_id)
        await message.answer(f"Привет, {name_users}!\n" \
                        "Твой промокод на 200рублей ‘БогданКодер’, активируй его в мобильном приложении CyberApp")
    else:
        await message.answer(f"{name_users}, ты уже получил промокод!")
    
    await session.close()



@bot.on.message(text=["получить", "бонус300"])
async def answer(message: Message, session: AsyncSession):
    name_users = (await bot.api.users.get(user_ids=message.from_id))[0].first_name
    if await get_user_number(session=session, user_id=message.from_id) is None:
        if await get_user_table(session=session, user_id=message.from_id) is None:
            await add_user_table(session=session, user_id=message.from_id, name=name_users)
    
        await message.answer(f"Привет, {name_users}! Для начисления депозита"
                        " поделись своим номером телефона в формате 799911112233, это будет твой логин в клубе!\n\n")
        await bot.state_dispenser.set(message.peer_id, SuperStates.NUMBER)
    else:
        await message.answer("На Ваш баланс уже зачислено 300р.")
        
    await session.close()



@bot.on.message(state=SuperStates.NUMBER)
async def name_handler(message: Message, session: AsyncSession):
    if re.match(r'^[78]\d{10}$', message.text):
        ctx.set("number", message.text)
        phone_number = ctx.get("number")
        if phone_number.startswith('8'):
                phone_number = '7' + phone_number[1:]
        await add_number(session=session, user_id=message.from_id, number=int(phone_number))
        await message.answer("На ваш баланс начислено 300р! Действует только в новом клубе по адресу Сеченова 10а! Следи за новостями в группе чтобы не пропустить дату открытия!")
        
        ctx.delete("number")
        await bot.state_dispenser.delete(message.peer_id)
        
    else:
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Вы ввели не верный формат телефона. Попробуйте еще раз!")

    await session.close()
    
    
@bot.on.message(text=["подписаться"])
async def unmut_bot(message: Message, session: AsyncSession):
    name_users = (await bot.api.users.get(user_ids=message.from_id))[0].first_name
    
    if await get_user_table(session=session, user_id=message.from_id) is None:
        await add_user_table(session=session, user_id=message.from_id, name=name_users)
    await unmute_bot(session=session, user_id=message.from_id)
    await message.answer("Вы успешно подписались на рассылку!")

    await session.close()


@bot.on.message(text=["отписаться"])
async def unmut_bot(message: Message, session: AsyncSession):
    if await is_mute_bot(session=session, user_id=message.from_id) == False:
        name_users = (await bot.api.users.get(user_ids=message.from_id))[0].first_name
        
        if await get_user_table(session=session, user_id=message.from_id) is None:
            await add_user_table(session=session, user_id=message.from_id, name=name_users)
        await mute_bot(session=session, user_id=message.from_id)
        await message.answer("Вы успешно отписались на рассылку!")
    else:
        await message.answer("Вы уже отписаны от рассылки!")
    
    await session.close()


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def handle_button_click(event: MessageEvent):
    if event.payload.get("type") == "reserve":

        await bot.api.messages.send(
            peer_id=settings.bot.ID_GROUP,
            message="Хочу забронировать!",
            random_id=0
        )
        # Ответ пользователю
        await event.show_snackbar("Ваш запрос на бронирование принят!")
    
    
if __name__ == "__main__":
    bot.labeler.message_view.register_middleware(DataBaseSession)
    bot.labeler.message_view.register_middleware(MessageLowRegister)
    bot.run_forever()
