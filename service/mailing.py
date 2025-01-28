import logging
import asyncio
import sys
import os

from vkbottle import Bot, API, Keyboard, Text, KeyboardButtonColor, PhotoMessageUploader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings



logging.getLogger("vkbottle").setLevel(logging.INFO)


def create_booking_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Хочу забронировать", payload={"type": "reserve"}), color=KeyboardButtonColor.POSITIVE)  # green button
    return keyboard.get_json()


async def get_all_members(group_id):
    members = []
    offset = 0
    count = 1000  # Максимальное количество пользователей за запрос
    
    while True:
        response = await api.groups.get_members(group_id=group_id, offset=offset, count=count)
        members.extend(response.items) 
        
        if offset + count >= response.count:
            break
        
        offset += count  

    return members


async def send_broadcast(message):
    users = await get_all_members(settings.bot.ID_GROUP)
    CHUNK_SIZE = 100
    for i in range(0, len(users), CHUNK_SIZE):
        chunk = users[i:i + CHUNK_SIZE]
        for id_user in chunk:
            try:
                photo = await photo_uploader.upload(file_source="photo.png", peer_id=0)
                await bot.api.messages.send(
                    user_id=id_user,
                    message=message,
                    keyboard=create_booking_keyboard(),
                    attachment=photo,
                    random_id=0
                )
                print(f"Сообщения отправлены пользователям: {id_user}")
            except Exception as e:
                print(f"Ошибка при отправке пользователям {id_user}: {e}")
            await asyncio.sleep(0.1)


api = API(settings.bot.TOKEN)
bot = Bot(api=api)
photo_uploader = PhotoMessageUploader(bot.api)


if __name__ == "__main__":
    message = "🔥 Супер скидка на общий зал!\n\n" \
            "Мы дарим скидку 50% на весь прайс общего зала в нашем клубе на ул. Сеченова, 10А 🎁\n\n" \
            "Успей забрать выгоду до 21 декабря включительно (пятница). Ждём тебя в клубе!"
    asyncio.run(send_broadcast(message=message))
