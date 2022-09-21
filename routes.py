from app import app
from flask import render_template, request, redirect, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import users, sections, threads

@app.route("/")
def index():
    return render_template("index.html", sections=sections.get_all_sections())


""" @app.route("/send", methods=["GET", "POST"])
def send():
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return "ei kirjauduttu"
    content = request.form["content"]
    sql = "INSERT INTO messages (content, sent_at, user_id) VALUES (:content, NOW(), :user_id)"
    db.session.execute(sql, {"content":content, "user_id": user_id})
    db.session.commit() 
    return redirect("/") """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return "Väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["user_role"]
        if password1 != password2:
            return "eri salasanat"
        password = password1
        hash_value = generate_password_hash(password)
        if users.register(username, password, role):
            return redirect("/")
        else:
            return "Tunnus jo käytössä"
    return redirect("/")


@app.route("/new_section", methods=["GET", "POST"])
def new_section():
    user_id = users.user_id()
    if users.is_admin() == 0:
        #TODO
        return "Ei oikeutta"   
    if request.method == "GET":
        return render_template("new_section.html")
    topic = request.form["topic"]
    section_id = sections.new_section(topic)
    return redirect("/")


@app.route("/new_thread<section_id>", methods=["GET", "POST"])
def new_thread():
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("new_thread.html")
    heading = request.form["heading"]
    sql = "INSERT INTO threads (heading, section_id, user_id) VALUES (:heading, :section_id, :user_id)"
    db.session.execute(sql, {"heading":heading, "section_id":section_id, "user_id":user_id})
    db.session.commit()
    return "Uusi alue luotu"

@app.route("/section/<int:section_id>")
def show_section(section_id):
    return("moi")

