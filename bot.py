import json
import logging
import signal

from dateutil import parser
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from master import aggregate_salaries

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '6948190992:AAEA0GdwkpnlQFnRnmffUsS6oT5k-S9j3U8'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        await update.message.reply_text('Привет! Отправьте JSON с датами и типом агрегации.')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    try:
        data = json.loads(update.message.text or '')
        dt_from = data.get('dt_from')
        dt_upto = data.get('dt_upto')
        group_type = data.get('group_type')

        if not all([dt_from, dt_upto, group_type]):
            await update.message.reply_text('Неверный формат данных. Отправьте JSON с полями dt_from, dt_upto и group_type.')
            return

        # Parse dates using dateutil
        try:
            dt_from_obj = parser.parse(dt_from)
            dt_upto_obj = parser.parse(dt_upto)
        except ValueError:
            await update.message.reply_text('Ошибка: Неверный формат даты.')
            return

        result = await aggregate_salaries(dt_from_obj, dt_upto_obj, group_type)

        if 'error' in result:
            await update.message.reply_text(f"Ошибка: {result['error']}")
        else:
            await update.message.reply_text(json.dumps(result))
    except json.JSONDecodeError:
        await update.message.reply_text('Ошибка: Неверный формат JSON.')
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await update.message.reply_text('Произошла ошибка при обработке вашего запроса.')


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    # Handle signals
    def signal_handler(sig, frame):
        logger.info("Received signal %s, stopping...", sig)
        application.run_polling()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
