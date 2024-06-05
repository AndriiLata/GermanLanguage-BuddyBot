import mysql.connector


# Connect with the database
def get_connection():
    conn = mysql.connector.connect(
        user='andrii',
        password='122002',
        host='localhost',
        database='users'
    )
    return conn


# Create table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        state INT,
        chat_id VARCHAR(255),
        name VARCHAR(255),
        language_level VARCHAR(255),
        file_id VARCHAR(255),
        personal_info TEXT,
        previous_profile VARCHAR(255),
        phone_number VARCHAR(255)
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


# Insert only previous_profile
def insert_previous_profile(chat_id, previous_profile):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users SET previous_profile = %s WHERE chat_id = %s
    ''', (previous_profile, chat_id))
    conn.commit()
    cursor.close()
    conn.close()


#get previous_profile
def get_previous_profile(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT previous_profile FROM users WHERE chat_id = %s
    ''', (chat_id,))
    previous_profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return previous_profile


def insert_user_data(user_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (state, chat_id, name, language_level, file_id, personal_info, phone_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (user_data['state'], user_data['chat_id'], user_data['name'], user_data['language_level'], user_data['file_id'], user_data['personal_info'], user_data['phone_number']))
    conn.commit()
    cursor.close()
    conn.close()
    print('User data inserted')


def create_table_matches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user1_chat_id VARCHAR(255),
        user2_chat_id VARCHAR(255)
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def insert_match(user1_chat_id, user2_chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO matches (user1_chat_id, user2_chat_id)
    VALUES (%s, %s)
    ''', (user1_chat_id, user2_chat_id))
    conn.commit()
    cursor.close()
    conn.close()


# get me all user2_chat_id with user1_chat_id
def get_matches(user1_chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user2_chat_id FROM matches WHERE user1_chat_id = %s
    ''', (user1_chat_id,))
    user2_chat_ids = cursor.fetchall()
    cursor.close()
    conn.close()
    return user2_chat_ids


def search_me(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE chat_id = %s
    ''', (chat_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# get my phone number with my chat_id
def get_phone_number(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT phone_number FROM users WHERE chat_id = %s
    ''', (chat_id,))
    phone_number = cursor.fetchone()
    cursor.close()
    conn.close()
    return phone_number


def delete_user(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users WHERE chat_id = %s
    ''', (chat_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_same_language_level(language_level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE language_level = %s
    ''', (language_level,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


