
from unittest import result
from app import app
from flask import render_template, request, redirect, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    sql = "SELECT content FROM messages"
    result = db.session.execute(sql)
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages)

@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return "ei kirjauduttu"
    content = request.form["content"]
    sql = "INSERT INTO messages (content, sent_at, user_id) VALUES (:content, NOW(), :user_id)"
    db.session.execute(sql, {"content":content, "user_id": user_id})
    db.session.commit() 
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # salasanan ja tunnuksen tarkistus
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return "Virheellinen tunnus"
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                print("oikea salasana")
                session["username"] = username 
                session["user_id"] = user.id
            else:
                print("väärä salasana")
        
        
        return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "eri salasanat"
        password = password1
        hash_value = generate_password_hash(password)
        try:
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
        except:
            return "tunnus jo käytössä"
    return redirect("/")