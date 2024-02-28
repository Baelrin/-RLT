from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json
import asyncio
from master import aggregate_salaries


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправьте JSON с датами и типом агрегации.')


async def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        data = json.loads(update.message.text)
        dt_from = data.get('dt_from')
        dt_upto = data.get('dt_upto')
        group_type = data.get('group_type')

        if not all([dt_from, dt_upto, group_type]):
            await update.message.reply_text('Неверный формат данных. Отправьте JSON с полями dt_from, dt_upto и group_type.')
            return

        result = await aggregate_salaries(dt_from, dt_upto, group_type)

        if 'error' in result:
            await update.message.reply_text(f"Ошибка: {result['error']}")
        else:
            await update.message.reply_text(json.dumps(result))
    except json.JSONDecodeError:
        await update.message.reply_text('Ошибка: Неверный формат JSON.')


async def main() -> None:
    updater = Updater(
        "6948190992:AAEA0GdwkpnlQFnRnmffUsS6oT5k-S9j3U8", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    await updater.start_polling()

    await updater.idle()

if __name__ == '__main__':
    asyncio.run(main())