import database


def get_user(language_level, chat_id):
    list_of_users = database.get_user_same_language_level(language_level)
    list_who_liked = [user_id[0] for user_id in database.get_matches(chat_id)]
    for user in list_of_users:
        if user[6] not in list_who_liked and user[6] != chat_id:
            return user


