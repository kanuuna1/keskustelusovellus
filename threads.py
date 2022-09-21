import imp
from db import db

def get_all_threads():
    sql = "SELECT * FROM threads"
    result = db.session.execute(sql).fetchall()
    return result

def new_thread(heading, section_id, user_id):
    sql = "INSERT INTO threads (heading, section_id, user_id) VALUES (:heading, :section_id, :user_id) RETURNING id"
    thread_id = db.session.execute(sql, {"heading":heading, "section_id":section_id, "user_id":user_id}).fetchone()[0]
    db.session.commit()
    return thread_id
