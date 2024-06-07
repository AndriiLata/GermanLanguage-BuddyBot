import database


def get_user(language_level, chat_id):
    list_of_users = database.get_user_same_language_level(language_level)
    list_who_liked = [user_id[0] for user_id in database.get_matches(chat_id)]
    for user in list_of_users:

        user_id = user[2]

        if isinstance(user_id, str):
            user_id = int(user_id)
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        #print(user_id, list_who_liked, chat_id)
        if user[2] not in list_who_liked and user_id != chat_id:
            return user


