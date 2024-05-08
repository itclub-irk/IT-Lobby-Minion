import json

from aiogram.types import Message

from src.settings import logger, WELCOME_MESSAGE_CONFIG_NAME, MAIN_CONFIG


@logger.catch
def get_buttons(buttons_config_name: str) -> dict:
    with open(buttons_config_name, 'r') as f:
        buttons = json.load(f)
    return buttons


def get_next_button_id(buttons: dict) -> str:
    if buttons:
        last_id = max(map(int, buttons.keys()))
        return str(last_id + 1)
    else:
        return "1"


def add_button(name: str, url: str, button_config_name: str):
    buttons = get_buttons(button_config_name)
    new_id = get_next_button_id(buttons)
    buttons[new_id] = {"name": name, "url": url}
    with open(button_config_name, 'w') as f:
        json.dump(buttons, f)
    return new_id


def remove_button(button_id: str, button_config_name: str):
    buttons = get_buttons(button_config_name)
    del buttons[button_id]
    with open(button_config_name, 'w') as f:
        json.dump(buttons, f)


def get_welcome_message_text(message: Message) -> str | None:
    with open(WELCOME_MESSAGE_CONFIG_NAME, 'r') as f:
        message_text = f.read()

    if not message_text:
        return None
    if message.from_user.username is not None:
        teg = f'@{message.from_user.username}'
    else:
        teg = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>'
    out_message = (f'🤖 <b>{message.from_user.full_name}</b> ({teg}) '
                   f'...connecting to <b>«{message.chat.title}»</b>. ' + message_text)
    return out_message


def set_welcome_message_text(message: str):
    with open(WELCOME_MESSAGE_CONFIG_NAME, 'w') as f:
        f.write(message)


def set_amount_of_dynamic_buttons(amount):
    with open(MAIN_CONFIG, 'w') as f:
        json.dump({'amount_of_dynamic_buttons': amount}, f)


def get_amount_of_dynamic_buttons() -> int:
    with open(MAIN_CONFIG, 'r') as f:
        config = json.load(f)
    return config['amount_of_dynamic_buttons']
