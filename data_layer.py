import sqlite3, bcrypt
from setting import CONNECTION_DATABASE


def is_valid_email(email):
    if email.count("@") != 1:
        return False

    at_index = email.index("@")
    if "." not in email[at_index + 1:]:
        return False

    return True


def hash_password(password, rounds=4):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds))
    return hashed.decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())




def get_blocked_users():
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE password LIKE '!:%'")
            rows = cursor.fetchall()

        return [r[0] for r in rows]

    except Exception as e:
        print(f"[*][get_blocked_users]Database error: {e}")
        return []





def get_user(username):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mail, password, authorization FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

        if row:
            return {
                "mail": row[0],
                "password": row[1],
                "authorization": row[2]
            }
        else:
            return None

    except Exception as e:
        print(f"Error from get_user: {e}")
        return None



def find_user_by_email(email):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, mail, password, authorization FROM users WHERE mail = ?", (email,))
            row = cursor.fetchone()

        if row:
            return {
                "username": row[0],
                "info": {
                    "mail": row[1],
                    "password": row[2],
                    "authorization": row[3]
                }
            }
        else:
            return {}

    except Exception as e:
        print(f"Error reading user data: {e}")
        return {}

def update_user(username, mail, password, authorization="normal_user", flag=True):
    if not is_valid_email(mail):
        print("Invalid email format.")
        return False

    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            exists = cursor.fetchone()
            if not exists:
                print("Username not found.")
                return False

            final_password = hash_password(password) if flag else password

            cursor.execute("""
                UPDATE users
                SET mail = ?, password = ?, authorization = ?
                WHERE username = ?
            """, (mail, final_password, authorization, username))

            conn.commit()
            return True

    except Exception as e:
        print(f"Database error in update_user: {e}")
        return False





def insert_user(username, mail, password, authorization="normal_user"):
    if not is_valid_email(mail):
        print("Invalid email format.")
        return False

    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            exists = cursor.fetchone()
            if exists:
                print("Username already exists.")
                return False

            hashed_password = hash_password(password)

            cursor.execute("""
                INSERT INTO users (username, mail, password, authorization)
                VALUES (?, ?, ?, ?)
            """, (username, mail, hashed_password, authorization))

            conn.commit()
            return True

    except Exception as e:
        print(f"Database error in insert_user: {e}")
        return False






def get_translation(en_word):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT meaning FROM translations WHERE word = ?", (en_word,))
            row = cursor.fetchone()

        return row[0] if row else None

    except Exception as e:
        print(f"Error reading dictionary from database: {e}")
        return None




def delete_translation(en_word):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM translations WHERE word = ?", (en_word,))
            exists = cursor.fetchone()
            if not exists:
                print("Word not found.")
                return False

            cursor.execute("DELETE FROM translations WHERE word = ?", (en_word,))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error deleting word from database: {e}")
        return False




def find_key_by_translation(fa_word):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM translations WHERE meaning = ?", (fa_word,))
            row = cursor.fetchone()

        return row[0] if row else None

    except Exception as e:
        print(f"Error reading dictionary from database: {e}")
        return None


def insert_translation(en_word, fa_word):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM translations WHERE word = ?", (en_word,))
            exists = cursor.fetchone()
            if exists:
                return False

            cursor.execute("INSERT INTO translations (word, meaning) VALUES (?, ?)", (en_word, fa_word))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error saving translation to database: {e}")
        return False



def update_translation(en_word, new_fa_word):
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM translations WHERE word = ?", (en_word,))
            exists = cursor.fetchone()
            if not exists:
                print("Word not found.")
                return False

            cursor.execute("UPDATE translations SET meaning = ? WHERE word = ?", (new_fa_word, en_word))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error updating dictionary in database: {e}")
        return False



def get_dictionary():
    try:
        with sqlite3.connect(CONNECTION_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word, meaning FROM translations")
            rows = cursor.fetchall()

        return {word: meaning for word, meaning in rows}

    except Exception as e:
        print(f"Error reading dictionary from database: {e}")
        return None
