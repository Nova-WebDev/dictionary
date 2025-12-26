import sqlite3
from setting import CONNECTION_DATABASE
from views.login_view import register_flow
from views.dashboard_view import main_menu_flow

def run_program(cursor):
    while True:
        token = register_flow(cursor)
        if token == "":
            break

        result = main_menu_flow(cursor, token)
        if not result:
            break

if __name__ == "__main__":
    conn = sqlite3.connect(CONNECTION_DATABASE)
    cursor = conn.cursor()

    run_program(cursor)

    conn.close()
