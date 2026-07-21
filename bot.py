import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN
from database import setup_database
from handlers import (
    start,
    addpost_button,
    post_text,
    post_time,
    cancel,
    auto_on,
    auto_off,
    POST_TEXT,
    POST_TIME
)
from scheduler import send_scheduled_post


def main():
    # Database Setup
    setup_database()

    # Application Builder
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start handler
    app.add_handler(CommandHandler("start", start))

    # Add Post Flow
    add_post_flow = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Add Post$"),
                addpost_button
            )
        ],
        states={
            POST_TEXT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    post_text
                )
            ],
            POST_TIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    post_time
                )
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    app.add_handler(add_post_flow)

    # Auto ON & OFF handlers
    app.add_handler(MessageHandler(filters.Regex("^▶️ Auto ON$"), auto_on))
    app.add_handler(MessageHandler(filters.Regex("^⛔ Auto OFF$"), auto_off))

    # Scheduler Job
    if app.job_queue:
        app.job_queue.run_repeating(
            send_scheduled_post,
            interval=60,
            first=10
        )

    print("Bot Started Successfully...")

    # Run Polling
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
