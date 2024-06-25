from aiogram import Bot


async def set_bot_description(bot: Bot):
    """
    Sets the description of the bot.

    :param bot: The bot object to set the description for.
    """
    await bot.set_my_description(
        "🤖 Я здесь, чтобы помочь вам эффективно управлять вашими финансами 💵\n\n"
        "Будем работать вместе 🤝, чтобы вы могли легко отслеживать свои доходы, "
        "контролировать расходы и принимать осознанные финансовые решения.\n\n"
        "Готовы начать? 🧐",
    )
