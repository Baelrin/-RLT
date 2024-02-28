from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import json
import asyncio
from master import aggregate_salaries


async def start(update: Update, context: CallbackContext) -> None:
    if update.message is not None:
        await update.message.reply_text('Привет! Отправьте JSON с датами и типом агрегации.')


async def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        if update.message is not None:
            data = json.loads(update.message.text or '')
        dt_from = data.get('dt_from')
        dt_upto = data.get('dt_upto')
        group_type = data.get('group_type')

        if not all([dt_from, dt_upto, group_type]):
            if update.message is not None:
                await update.message.reply_text('Неверный формат данных. Отправьте JSON с полями dt_from, dt_upto и group_type.')
            return

        result = await aggregate_salaries(dt_from, dt_upto, group_type)

        if update.message is not None:
            if 'error' in result:
                await update.message.reply_text(f"Ошибка: {result['error']}")
            else:
                await update.message.reply_text(json.dumps(result))
    except json.JSONDecodeError:
        if update.message is not None:
            await update.message.reply_text('Ошибка: Неверный формат JSON.')


async def main() -> None:
    updater = Updater(
        "6948190992:AAEA0GdwkpnlQFnRnmffUsS6oT5k-S9j3U8")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        filters.text & ~filters.command, handle_message))

    await updater.start_polling()

    while True:
        await asyncio.sleep(60)  # Ожидание 60 секунд перед следующей итерацией

if __name__ == '__main__':
    asyncio.run(main())
