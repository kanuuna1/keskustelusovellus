from secrets import token_hex
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, username, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["is_admin"] = user.role
            session["csrf_token"] = token_hex(16)
            return True
    return False


def logout():
    del session["user_id"]
    del session["username"]
    del session["is_admin"]
    del session["csrf_token"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def is_admin():
    return session.get("is_admin")

def check_csrf_token(request):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_id_by_name(username):
    sql = "SELECT id FROM users WHERE username=:username"
    return db.session.execute(sql, {"username":username}).fetchone()[0]
