import time
import logging
import requests
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(dotenv_path="../.env")

from database.engine import session
from database.querys import is_mute_bot
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

TOKEN = config.BOT_TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_group_members(group_id: int = 227822517):
    members = vk.groups.getMembers(group_id=group_id)
    return members['items']


def get_user_year(user_id):
    user_info = vk.users.get(user_ids=user_id, fields="bdate")[0]
    if 'bdate' in user_info:
        bdate = user_info['bdate']

        if len(bdate.split('.')) == 3:
            birth_date = datetime.strptime(bdate, '%d.%m.%Y')
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        else:
            log.info(f"Год рождения не указан у пользовтеля {user_id}")
    else:
        log.info(f"День рождение у пользователя не указан{user_id}")


def get_citi_year(user_id):
    user_info = vk.users.get(user_ids=user_id, fields="city")[0]

    if 'city' in user_info:
        city_name = user_info['city']['title']
        return city_name
    else:
        log.info(f"Город не указан у пользователя {user_id}")


def upload_photo_to_vk(photo_path):
    upload_url = vk.photos.getMessagesUploadServer()['upload_url']

    with open(photo_path, 'rb') as file:
        response = requests.post(upload_url, files={'photo': file}).json()

    photo_info = vk.photos.saveMessagesPhoto(
        photo=response['photo'],
        server=response['server'],
        hash=response['hash']
    )[0]

    attachment = f"photo{photo_info['owner_id']}_{photo_info['id']}"
    return attachment


def send_broadcast_message(user_ids, photo_path: str):
    attachment = upload_photo_to_vk(photo_path)
    for user_id in user_ids:
        try:
            with session() as session_:
                if is_mute_bot(session=session_, user_id=user_id) == False:
                    if get_citi_year(user_id) == 'Новокузнецк' and get_user_year(user_id) <= 20:
                        vk.messages.send(
                            user_id=user_id,
                            message=f"Привет, {vk.users.get(user_ids=user_id)[0]['first_name']}! Ты получил сообщение рассылку!",
                            attachment=attachment,
                            random_id=vk_api.utils.get_random_id()
                        )
                        time.sleep(0.05)
                        log.info(f"Cообщение отправлено пользоателя, {user_id}")
                    else:
                        log.info(f"Пользователя {user_id} не подходит под условие")
                else:
                    log.info(f"Пользователя {user_id} заблокировал бота")
        except vk_api.exceptions.ApiError as e:
            log.info(f"Ошибка при отправке пользователю {user_id}: {e}")


if __name__ == "__main__":
    send_broadcast_message(
        user_ids=get_group_members(),
        photo_path="imperia.jpg"
    )
    log.info("Бот отработал!")