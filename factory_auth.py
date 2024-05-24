from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



auth = HTTPBasicAuth()

users = {
    "ahmed": generate_password_hash("ahm123"),
    "nitro": generate_password_hash("nit123")
}


@auth.verify_password
def verify_pass(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return  username