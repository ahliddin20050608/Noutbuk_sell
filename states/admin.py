from aiogram.fsm.state import StatesGroup, State


class AddLaptop(StatesGroup):
    title = State()
    description = State()
    brand = State()
    cpu = State()
    ram = State()
    storage = State()
    gpu = State()
    price = State()
    quantity = State()
    image = State()
    status = State()
    type_ = State()





class SendToUser(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_message = State()
