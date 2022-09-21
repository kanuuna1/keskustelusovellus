import imp
from db import db

def new_section(topic):
    sql = "INSERT INTO sections (topic) VALUES (:topic) RETURNING id"
    section_id = db.session.execute(sql, {"topic":topic}).fetchone()[0]
    db.session.commit()
    return section_id

def get_all_sections():
    sql = "SELECT topic FROM sections"
    result = db.session.execute(sql).fetchall()
    return result

def count_threads(section_id):
    sql = "SELECT COUNT(*) FROM threads WHERE section_id = :section_id"
    return db.session.execute(sql, {"section_id":section_id})