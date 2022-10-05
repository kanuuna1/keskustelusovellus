from crypt import methods
from importlib.resources import read_binary
from app import app
from flask import render_template, request, redirect, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import users, sections, threads, messages

@app.route("/")
def index():
    #TODO: näytä ketjujen ja viestin määrä ja viimeisimmän viestin ajankohta
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
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")
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
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
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
    if len(topic) < 1 or len(topic) > 40:
            return render_template("error.html", message="Otsikossa tulee olla 1-40 merkkiä")
    section_id = sections.new_section(topic)
    users.check_csrf_token(request)
    return redirect("/")

@app.route("/section/<int:section_id>")
def show_section(section_id):
    #TODO: näytä muokkaus/poistomahdollisuus
    return render_template("threads.html", section_id=section_id, topic=sections.get_topic(section_id), threads=threads.get_all_threads(section_id))

@app.route("/new_thread/<int:section_id>", methods=["GET", "POST"])
def new_thread(section_id):
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("new_thread.html", section_id=section_id)    
    heading = request.form["heading"]
    if len(heading) < 1 or len(heading) > 40:
        return render_template("error.html", message="Otsikossa tulee olla 1-40 merkkiä")
    thread_id = threads.new_thread(heading, section_id, user_id)
    users.check_csrf_token(request)
    return redirect("/")

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    #TODO:näytä viestien tiedot?
    return render_template("messages.html", thread_id=thread_id, title=threads.get_heading(thread_id), messages=messages.get_all_messages(thread_id))

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("edit_thread.html", thread_id=thread_id, thread_user_id=threads.get_user_id(thread_id))
    heading = request.form["heading"]
    if len(heading) < 1 or len(heading) > 40:
        return render_template("error.html", message="Otsikossa tulee olla 1-40 merkkiä")
    users.check_csrf_token(request)
    threads.edit_thread(thread_id, heading)
    return redirect("/")

@app.route("/remove_thread/<int:thread_id>", methods=["GET", "POST"])
def remove_thread(thread_id):
    user_id = users.user_id()
    #users.check_csrf_token(request)
    threads.remove_thread(thread_id, user_id)
    return redirect("/")

@app.route("/new_message/<int:thread_id>", methods=["GET", "POST"])
def new_message(thread_id):
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("new_message.html", thread_id=thread_id)
    content = request.form["content"]
    if len(content) < 1 or len(content) > 500:
        return render_template("Viestissä tulee olla 1-500 merkkiä")
    message_id = messages.new_message(content, user_id, thread_id)
    users.check_csrf_token(request)
    return redirect("/thread/"+str(thread_id))

@app.route("/remove_message/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    user_id = users.user_id()
    #TODO: csrf-check?
    #users.check_csrf_token(request)
    messages.remove_message(message_id, user_id)
    return redirect("/")

@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    user_id = users.user_id()
    if request.method == "GET":
        return render_template("edit_message.html", message_user_id=messages.get_user_id(message_id), content=messages.get_content(message_id), message_id=message_id)
    content = request.form["content"]
    if len(content) < 1 or len(content) > 500:
        return render_template("Viestissä tulee olla 1-500 merkkiä")
    message_id = request.form["message_id"]
    users.check_csrf_token(request)
    messages.edit_message(message_id, user_id, content)
    return redirect("/")


