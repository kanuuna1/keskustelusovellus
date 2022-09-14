from crypt import methods
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
    content = request.form["content"]
    sql = "INSERT INTO messages (content, sent_at) VALUES (:content, NOW())"
    db.session.execute(sql, {"content":content})
    db.session.commit() 
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
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
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        
    return "rekisteroity"