# handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import OWNER_ID

from database import (
    add_subscriber,
    get_admins,
    add_post,
    add_admin,
    remove_admin,
    update_settings
)


POST_TEXT = 1
POST_TIME = 2



def is_admin(user_id):

    if user_id == OWNER_ID:
        return True

    admins = get_admins()

    return user_id in [x[0] for x in admins]



def private_only(update):

    return update.effective_chat.type == "private"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if is_admin(user_id) and private_only(update):

        keyboard = [

            ["➕ Add Post"],

            ["📋 Posts"],

            ["▶️ Auto ON", "⛔ Auto OFF"],

            ["⚙️ Settings"],

            ["👥 Groups", "👤 Admins"]

        ]


        await update.message.reply_text(

            "🤖 Bot Control Panel",

            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )

        )

    else:

        if private_only(update):

            add_subscriber(user_id)

            await update.message.reply_text(
                "✅ Subscription activated."
            )



async def addpost_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return ConversationHandler.END


    await update.message.reply_text(
        "📝 পোস্টের টেক্সট পাঠান:"
    )

    return POST_TEXT



async def post_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["post_text"] = update.message.text


    await update.message.reply_text(
        "⏱ কত মিনিট পর পর পোস্ট হবে?"
    )

    return POST_TIME



async def post_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    minutes = int(update.message.text)

    text = context.user_data["post_text"]


    add_post(
        text,
        None,
        minutes
    )


    await update.message.reply_text(
        "✅ Post Added Successfully"
    )


    return ConversationHandler.END



async def cancel(update, context):

    await update.message.reply_text(
        "Cancelled"
    )

    return ConversationHandler.END



async def auto_on(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return


    update_settings(
        enabled=1
    )


    await update.message.reply_text(
        "✅ Auto Post ON"
    )



async def auto_off(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return


    update_settings(
        enabled=0
    )


    await update.message.reply_text(
        "⛔ Auto Post OFF"
    )



async def add_admin_command(update, context):

    if not is_admin(update.effective_user.id):
        return


    if context.args:

        user_id = int(context.args[0])

        add_admin(user_id)


        await update.message.reply_text(
            "✅ Admin Added"
        )