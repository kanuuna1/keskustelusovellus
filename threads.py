import imp
from db import db

def get_all_threads(section_id):
    sql = "SELECT * FROM threads WHERE section_id=:section_id"
    result = db.session.execute(sql, {"section_id":section_id}).fetchall()
    db.session.commit()
    return result

def new_thread(heading, section_id, user_id):
    sql = "INSERT INTO threads (heading, section_id, user_id) VALUES (:heading, :section_id, :user_id) RETURNING id"
    thread_id = db.session.execute(sql, {"heading":heading, "section_id":section_id, "user_id":user_id}).fetchone()[0]
    db.session.commit()
    return thread_id



