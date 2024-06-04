import database


def get_user(language_level, chat_id):
    list_of_users = database.get_user_same_language_level(language_level)
    for user in list_of_users:
        if user[6] != chat_id:
            return user