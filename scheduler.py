# scheduler.py

from database import (
    get_settings,
    get_posts,
    get_groups,
    get_subscribers,
    update_current_post
)


async def send_scheduled_post(context):

    settings = get_settings()

    if not settings:
        return


    enabled, current_post, welcome, send_private = settings


    if enabled == 0:
        return


    posts = get_posts()


    if not posts:
        return


    post = posts[current_post % len(posts)]


    post_id = post[0]
    text = post[1]
    photo = post[2]


    # Send to groups

    for group in get_groups():

        chat_id = group[0]

        try:

            if photo:

                await context.bot.send_photo(
                    chat_id,
                    photo,
                    caption=text
                )

            else:

                await context.bot.send_message(
                    chat_id,
                    text
                )


        except Exception as e:

            print(e)



    # Send to subscribers

    if send_private:

        for user in get_subscribers():

            try:

                await context.bot.send_message(
                    user[0],
                    text
                )

            except Exception as e:

                print(e)



    update_current_post(
        (current_post + 1) % len(posts)
    )