from aiogram.fsm.state import StatesGroup, State


class FSM_admin_panel(StatesGroup):
    get_message = State()
    edit_buttons = State()
    delete_buttons = State()
    get_button_name = State()
    get_button_link = State()