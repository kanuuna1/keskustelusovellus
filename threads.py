from db import db

def get_all_threads(section_id):
    sql = "SELECT * FROM threads WHERE section_id=:section_id AND visible=TRUE"
    result = db.session.execute(sql, {"section_id":section_id}).fetchall()
    db.session.commit()
    return result

def new_thread(heading, section_id, user_id):
    sql = "INSERT INTO threads (heading, section_id, user_id, visible) VALUES (:heading, :section_id, :user_id, TRUE) RETURNING id"
    thread_id = db.session.execute(sql, {"heading":heading, "section_id":section_id, "user_id":user_id}).fetchone()[0]
    db.session.commit()
    return thread_id

def get_heading(thread_id):
    id = thread_id
    sql = "SELECT heading FROM threads WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def get_section_id(thread_id):
    id = thread_id
    sql = "SELECT section_id FROM threads WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def get_user_id(thread_id):
    id = thread_id
    sql = "SELECT user_id FROM threads WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def remove_thread(id, user_id):
    sql = "UPDATE threads SET visible=FALSE WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()

def edit_thread(id, heading):
    sql = "UPDATE threads SET heading=:heading WHERE id=:id"
    db.session.execute(sql, {"id":id, "heading":heading})
    db.session.commit()
