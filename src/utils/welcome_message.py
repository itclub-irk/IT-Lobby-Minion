from src.database.models import DbSettings


async def configure_welcome_message(
        user_full_name: str, username: str = None, user_id: int = None
) -> str:
    welcome_message_text = (await DbSettings.get_settings()).welcome_message

    welcome_message_text = welcome_message_text.replace(
        '{{NAME}}', user_full_name
    ).replace(
        '{{USERNAME}}', f'@{username}'
        if username
        else f'<a href="tg://user?id={user_id}">{user_full_name}</a>'
    )

    return welcome_message_text
