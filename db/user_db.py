import sqlite3
from setting import CONNECTION_DATABASE


def get_role_id_by_name(role_name):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM roles WHERE role_name = ?", (role_name,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_role_id_by_name]Database error: role_name not found in roles table")
        return result[0]


def get_all_users():
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.password, r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
        """)
        rows = cursor.fetchall()

        result = {}
        for row in rows:
            user_id = row[0]
            result[user_id] = {
                "username": row[1],
                "email": row[2],
                "password": row[3],
                "role": row[4]
            }
        return result


def get_user_role(username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role_name
            FROM user_roles_view
            WHERE username = ?
        """, (username,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_user_role]Database error: username not found in user_roles_view")
        return result[0]


def get_username_by_email(email):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username FROM users WHERE email = ?
        """, (email,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_username_by_email]Database error: email not found in users table")
        return result[0]


def get_user_credentials(username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT email, password FROM users WHERE username = ?
        """, (username,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_user_credentials]Database error: username not found in users table")
        return {
            "email": result[0],
            "password": result[1]
        }


def get_user_id_by_username(username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM users WHERE username = ?
        """, (username,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_user_id_by_username]Database error: username not found in users table")
        return result[0]


def get_all_blocked_users():
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password FROM users
        """)
        rows = cursor.fetchall()

        result = {}
        for row in rows:
            user_id, username, password = row
            if password.startswith("!:"):
                result[user_id] = username

        return result


def insert_user(username, email, password, role_name):
    role_id = get_role_id_by_name(role_name)
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            INSERT INTO users (username, email, password, role_id)
            VALUES (?, ?, ?, ?)
        """, (username, email, password, role_id))


def update_user_by_id(user_id, fields):
    if not fields:
        return

    updates = []
    values = []

    if "email" in fields:
        updates.append("email = ?")
        values.append(fields["email"])

    if "password" in fields:
        updates.append("password = ?")
        values.append(fields["password"])

    if "role_name" in fields:
        role_id = get_role_id_by_name(fields["role_name"])
        updates.append("role_id = ?")
        values.append(role_id)

    values.append(user_id)

    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE users
            SET {', '.join(updates)}
            WHERE id = ?
        """, values)


def block_user_by_id(user_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT password FROM users WHERE id = ?
        """, (user_id,))
        result = cursor.fetchone()

        if not result:
            raise Exception("[*][block_user_by_id]Database error: user_id not found in users table")

        current_password = result[0]
        if current_password.startswith("!:"):
            raise Exception("[*][block_user_by_id]Database error: user is already blocked")

        blocked_password = "!:" + current_password

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (blocked_password, user_id))


def unblock_user_by_id(user_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT password FROM users WHERE id = ?
        """, (user_id,))
        result = cursor.fetchone()

        if not result:
            raise Exception("[*][unblock_user_by_id]Database error: user_id not found in users table")

        password = result[0]
        if not password.startswith("!:"):
            raise Exception("[*][unblock_user_by_id]Database error: user is not blocked")

        new_password = password[2:]  # حذف !:

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (new_password, user_id))
