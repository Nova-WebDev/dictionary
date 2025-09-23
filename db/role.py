import sqlite3
from setting import CONNECTION_DATABASE

def get_all_roles():
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, role_name FROM roles")
        rows = cursor.fetchall()

        return [{"id": row[0], "role_name": row[1]} for row in rows]


def role_id_exists(role_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM roles WHERE id = ?", (role_id,))
        return cursor.fetchone() is not None

def get_role_name_by_id(role_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role_name FROM roles WHERE id = ?", (role_id,))
        result = cursor.fetchone()
        if not result:
            raise Exception("[*][get_role_name_by_id]Database error: role_id not found in roles table")
        return result[0]