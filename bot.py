# bot.py

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



from telegram.ext import ApplicationBuilder


def main():
    # আপনার টোকেন
    app = (
        ApplicationBuilder().token("8211501288:AAGP3VnpZbVu41jVRbu9TxyE8Dox7UjcT98").build()
    )

    # আপনার হ্যান্ডলার যুক্ত করুন...

    # রান পোলিং
    app.run_polling()


if __name__ == "__main__":
    main()

asasas# /start

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


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

            CommandHandler(
                "cancel",
                cancel
            )

        ]

    )


    app.add_handler(
        add_post_flow
    )


    # Auto ON

    app.add_handler(
        MessageHandler(
            filters.Regex("^▶️ Auto ON$"),
            auto_on
        )
    )


    # Auto OFF

    app.add_handler(
        MessageHandler(
            filters.Regex("^⛔ Auto OFF$"),
            auto_off
        )
    )


    # Scheduler test

    app.job_queue.run_repeating(
        send_scheduled_post,
        interval=60,
        first=10
    )


    print(
        "Bot Started Successfully..."
    )


    app.run_polling()



if __name__ == "__main__":
    main()
