import time
import sys
import os
import logging
from dotenv import load_dotenv
from collections import defaultdict

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(dotenv_path="../.env")

from config import config
from database.querys import (
    get_user_table,
    add_user_table,
    get_user_table_promocode,
    add_user_table_promocode,
    add_number,
    mute_bot,
    unmute_bot,
    is_mute_bot,
    get_user_number
)
from database.engine import session
from utils.valid_phone_number import is_valid_phone_number

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

TOKEN = config.BOT_TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

user_message_log = defaultdict(list)

user_ban_log = {}
confirmation = {}


def create_confirmation_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def get_user_name(user_id):
    user_info = vk.users.get(user_ids=user_id)
    first_name = user_info[0]['first_name']
    return first_name


def is_spam(user_id):
    current_time = time.time()

    if user_id in user_ban_log:
        ban_start = user_ban_log[user_id]
        if current_time - ban_start < config.message_settings.BAN_TIME:
            return True
        else:
            del user_ban_log[user_id]

    user_message_log[user_id].append(current_time)

    user_message_log[user_id] = [t for t in user_message_log[user_id] if
                                current_time - t <= config.message_settings.TIME_LIMIT]
    if len(user_message_log[user_id]) > config.message_settings.MESSAGE_LIMIT:
        user_ban_log[user_id] = current_time
        return True

    return False


def send_message(user_id, message, keyboard: VkKeyboard | None = None):
    if is_spam(user_id):
        vk.messages.send(
            user_id=user_id,
            message="Вы отправляете слишком много сообщений. Подождите немного (1 мин).",
            random_id=vk_api.utils.get_random_id(),
        )
    else:
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=vk_api.utils.get_random_id(),
            keyboard=keyboard,
        )


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message = event.text.lower()
            if message == '+':
                with session() as session_:
                    if get_user_table(session=session_, user_id=user_id) is None:
                        add_user_table(session=session_, user_id=user_id, name=get_user_name(event.user_id))
                    if get_user_table_promocode(session=session_, user_id=user_id) is None:
                        add_user_table_promocode(session=session_, user_id=user_id)
                        promo_message = f"Привет, {get_user_name(event.user_id)}!\n" \
                        "Твой промокод на 200рублей ‘БогданКодер’, активируй его в мобильном приложении CyberApp"
                    else:
                        promo_message = f"{get_user_name(event.user_id)}, ты уже получил промокод!"
                send_message(user_id, promo_message)

            if message == "подписаться":
                with session() as session_:
                    if get_user_table(session=session_, user_id=user_id) is None:
                        add_user_table(session=session_, user_id=user_id, name=get_user_name(event.user_id))
                    unmute_bot(session=session_, user_id=user_id)
                    send_message(user_id, "Вы успешно подписались на рассылку!")
            elif message == "отписаться" or message == "отписка":
                with session() as session_:
                    if is_mute_bot(session=session_, user_id=user_id) == False:
                        confirmation[user_id] = True
                        send_message(
                            user_id,
                            "Вы уверены, что хотите отписаться?",
                            keyboard=create_confirmation_keyboard()
                        )
                    else:
                        send_message(user_id, "Вы не были подписаны на рассылку.")
            elif user_id in confirmation:
                if message == "да":
                    with session() as session_:
                        mute_bot(session=session_, user_id=user_id)
                        send_message(user_id, "Вы успешно отписались от рассылки!")

                        confirmation.pop(user_id)
                elif message == "нет":
                    send_message(user_id, "Ваша подписка на рассылку сохраняется!")
            
            if message == "получить":
                with session() as session_:
                    if get_user_table(session=session_, user_id=user_id) is None:
                        add_user_table(session=session_, user_id=user_id, name=get_user_name(event.user_id))
                send_message(user_id, "Поделитесь своим номером телефона в формате - 79991112233")
            elif is_valid_phone_number(message):
                with session() as session_:
                    if get_user_number(session=session_, number=int(message)) is None:
                        add_number(session=session_, user_id=user_id, number=int(message))
                        send_message(user_id, "Мы запомнили ваш номер телефона!")
                    else:
                        send_message(user_id, "Вы уже ввели этот номер телефона.")
            elif message.isdigit() and (len(message) >= 7 and len(message)<=10):
                send_message(user_id, "Формат вашего номера не верный!")


if __name__ == "__main__":
    log.info("Бот запустился")
    main()
