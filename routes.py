from app import app
from flask import render_template, request, redirect, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import users, sections, threads

@app.route("/")
def index():
    return render_template("index.html", sections=sections.get_all_sections())

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
            return render_template("error.html", message="Väärä tunnus tai salasana")

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
            return render_template("error.html", message="Tunnus jo käytössä")
    return redirect("/")


@app.route("/new_section", methods=["GET", "POST"])
def new_section():
    user_id = users.user_id()
    if users.is_admin() == 0:
        #TODO
        return render_template("error.html", message="Ei käyttöoikeutta")  
    if request.method == "GET":
        return render_template("new_section.html")
    topic = request.form["topic"]
    section_id = sections.new_section(topic)
    return redirect("/")

@app.route("/section/<int:section_id>")
def show_section(section_id):
    #TODO: näytä alueen nimi?
    #topic = sections.get_topic(section_id)
    return render_template("threads.html", threads=threads.get_all_threads(section_id))

@app.route("/new_thread/<section_id>", methods=["GET", "POST"])
def new_thread(section_id):
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("new_thread.html", section_id=section_id)    
    heading = request.form["heading"]
    thread_id = threads.new_thread(heading, section_id, user_id)
    return redirect("/")



