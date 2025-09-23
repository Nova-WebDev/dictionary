from views.login_view import register_flow
from views.dashboard_view import main_menu_flow

def run_program():
    while True:
        token = register_flow()
        if token == "":
            break

        result = main_menu_flow(token)
        if not result:
            break


if __name__ == "__main__":
    run_program()
