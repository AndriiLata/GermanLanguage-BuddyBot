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
        personal_info TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def insert_user_data(user_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (state, chat_id, name, language_level, file_id, personal_info)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', (user_data['state'], user_data['chat_id'], user_data['name'], user_data['language_level'], user_data['file_id'], user_data['personal_info']))
    conn.commit()
    cursor.close()
    conn.close()


def search_user(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE chat_id = %s
    ''', (chat_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


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


