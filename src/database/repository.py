import json
from typing import List, Tuple

from aiogram.types import Message


def get_buttons() -> dict:
    with open('src/database/buttons.json', 'r') as f:
        buttons = json.load(f)
    return buttons


def get_next_button_id(buttons: dict) -> str:
    if buttons:
        last_id = max(map(int, buttons.keys()))
        return str(last_id + 1)
    else:
        return "1"


def add_button(name: str, url: str):
    buttons = get_buttons()
    new_id = get_next_button_id(buttons)
    buttons[new_id] = {"name": name, "url": url}
    with open('src/database/buttons.json', 'w') as f:
        json.dump(buttons, f)
    return new_id


def remove_button(button_id: str):
    buttons = get_buttons()
    del buttons[button_id]
    with open('src/database/buttons.json', 'w') as f:
        json.dump(buttons, f)


def get_welcome_message_text(message: Message) -> str | None:
    with open('src/database/welcome_message.txt', 'r') as f:
        message_text = f.read()

    if not message_text:
        return None

    out_message = (f'🤖 <b>{message.from_user.full_name}</b> (@{message.from_user.username}) '
                   f'...connecting to <b>«{message.chat.title}»</b>. ' + message_text)
    return out_message


def set_welcome_message_text(message: str):
    with open('src/database/welcome_message.txt', 'w') as f:
        f.write(message)
