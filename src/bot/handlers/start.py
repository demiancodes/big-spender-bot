from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import MAIN_MENU_KB

router = Router()

START_MESSAGE = (
    "🖖 Добро пожаловать в систему учета и анализа доходов и расходов!\n\n"
    "Для получения необходимой информации, а также для добавления доходов и расходов, "
    "нажмите на интересующий раздел 👇👇"
)


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    """
    Handles the /start command by sending a welcome message and the MAIN_MENU_KB object to display
    the main menu keyboard.

    Clears the current state of the Finite State Machine (FSM), removing any stored state
    information. This allows for starting the interaction with the user from a clean slate,
    disregarding previous actions or states.

    :param message: A Message object from the Telegram API, representing the incoming message.
    :param state: FSM context to manage the state of the finite state machine.
    """
    await state.clear()
    await message.answer(text=START_MESSAGE, reply_markup=MAIN_MENU_KB)
