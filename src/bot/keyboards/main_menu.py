from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_MENU_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить транзакцию", callback_data="add_transaction")],
        [
            InlineKeyboardButton(text="💰 Кошелек", callback_data="wallet"),
            InlineKeyboardButton(text="💸 Расходы", callback_data="expenses"),
        ],
        [
            InlineKeyboardButton(text="📑 Категории", callback_data="categories"),
            InlineKeyboardButton(text="📊 Отчеты", callback_data="reports"),
        ],
    ],
)
