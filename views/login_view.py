from logic.auth import login_user, sign_in_user, initiate_password_reset, complete_password_reset

def register_flow():
    while True:
        print("""
1) Log in
2) Sign up
3) Forgot password
0) Exit
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                token = login_user(username, password)
                if token:
                    print("Login successful.")
                    return token
                else:
                    print("Login failed.")
            except Exception as e:
                print("[*][login_user] Error:", e)

        elif choice == "2":
            try:
                username = input("Username: ").strip()
                email = input("Email address: ").strip()
                password = input("Password: ").strip()
                token = sign_in_user(username, email, password)
                if token:
                    print("Registration successful.")
                    return token
                else:
                    print("Registration failed.")
            except Exception as e:
                print("[*][sign_in_user] Error:", e)

        elif choice == "3":
            try:
                email = input("What's your email address: ").strip()
                code = initiate_password_reset(email)
                if not code:
                    print("Reset initiation failed.")
                    continue

                for attempt in range(3):
                    user_code = input("Enter the code sent to your email: ").strip()
                    if user_code == code:
                        break
                    print("Incorrect code.\n")
                else:
                    print("Too many failed attempts. Password reset aborted.")
                    continue

                new_password = input("Enter your new password: ").strip()
                token = complete_password_reset(email, code, user_code, new_password)
                if token:
                    print("Password reset successful.")
                    return token
                else:
                    print("Password reset failed.")
            except Exception as e:
                print("[*][forget_password] Error:", e)

        elif choice == "0":
            print("Goodbye.")
            return ""

        else:
            print("Invalid option. Please try again.")
