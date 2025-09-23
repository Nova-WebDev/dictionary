import json, bcrypt, time, random, smtplib
from email.mime.text import MIMEText
from cryptography.hazmat.primitives import serialization
from setting import PRIVATE_KEY_PATH, PRIVATE_KEY_PASSWORD, TOKEN_EXPIRATION, BCRYPT_SALT_ROUNDS, SENDER_EMAIL, \
    APP_PASSWORD
from db.user_db import get_user_role, get_user_credentials, user_exists, email_exists, insert_user, \
    get_user_id_by_username, get_username_by_email, update_user_by_id


def sign_payload(payload_json):
    with open(PRIVATE_KEY_PATH, "rb") as f:
        password_bytes = PRIVATE_KEY_PASSWORD.encode("utf-8")
        private_key = serialization.load_pem_private_key(f.read(), password=password_bytes)

    signature = private_key.sign(payload_json.encode("utf-8"))
    return signature.hex()

def build_token(username):
    role = get_user_role(username)
    now = int(time.time())
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + TOKEN_EXPIRATION,
        "iss": "auth"
    }
    payload_json = json.dumps(payload, separators=(",", ":"))
    signature_hex = sign_payload(payload_json)
    return payload_json + "." + signature_hex

def login_user(username, password):
    if not user_exists(username):
        return ""

    creds = get_user_credentials(username)

    if not bcrypt.checkpw(password.encode(), creds["password"]):
        return ""

    token = build_token(username)
    return token or ""



def sign_in_user(username, email, password):
    if "@" not in email or "." not in email or email.index("@") > email.rindex("."):
        return ""

    if user_exists(username):
        return ""

    if email_exists(email):
        return ""

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_SALT_ROUNDS)).decode()
    insert_user(username, email, hashed_password, role_name="normal_user")

    token = build_token(username)
    return token or ""


def send_recovery_email(username, email, code):
    message = MIMEText(
        f"Hi {username}!\n\nYour recovery code is: {code}\n\nIf you didn’t request this, just ignore it.")
    message["Subject"] = "Password Reset Code"
    message["From"] = SENDER_EMAIL
    message["To"] = email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(message)
    server.quit()

def initiate_password_reset(email):
    if not email_exists(email):
        return ""

    username = get_username_by_email(email)
    creds = get_user_credentials(username)

    if creds["password"].startswith("!:"):
        return ""

    code = str(random.randrange(1000, 10000))
    send_recovery_email(username, email, code)
    return code

def complete_password_reset(email, code, user_code, new_password):
    if user_code != code:
        return ""

    username = get_username_by_email(email)
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    user_id = get_user_id_by_username(username)
    update_user_by_id(user_id, {"password": hashed})

    token = build_token(username)
    return token or ""

