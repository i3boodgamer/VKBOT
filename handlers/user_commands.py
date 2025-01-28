from vkbottle.bot import Message, BotLabeler, Bot


labelar = BotLabeler()


@labelar.message(text=["Получить", "получить"])
async def answer(message: Message):
    await message.answer("Привет!")


@labelar.message(text="+")
async def answer(message: Message):
    await message.answer(f"Привет, !\n" \
                        "Твой промокод на 200рублей ‘БогданКодер’, активируй его в мобильном приложении CyberApp")