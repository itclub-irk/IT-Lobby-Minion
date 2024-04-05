import json
from typing import List, Tuple

from aiogram.types import Message


def get_buttons() -> dict:
    with open('src/database/buttons.json', 'r') as f:
        buttons = json.load(f)
    return buttons


def add_button(name: str, url: str):
    buttons = get_buttons()
    buttons[name] = url
    with open('src/database/buttons.json', 'w') as f:
        json.dump(buttons, f)


def remove_button(*button_names: Tuple[str] | str):
    buttons = get_buttons()
    for button_name in button_names:
        buttons.pop(button_name, None)
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
