from db import db

def new_section(topic):
    sql = "INSERT INTO sections (topic, visible) VALUES (:topic, TRUE) RETURNING id"
    section_id = db.session.execute(sql, {"topic":topic}).fetchone()[0]
    db.session.commit()
    return section_id

def get_all_sections():
    sql = "SELECT * FROM sections WHERE visible=TRUE"
    result = db.session.execute(sql).fetchall()
    return result

def count_threads(section_id):
    id = section_id
    sql = "SELECT COUNT(*) FROM threads WHERE id=:id"
    return db.session.execute(sql, {"section_id":id}).fetchone()

#TODO
def get_topic(section_id):
    id = section_id
    sql = "SELECT topic FROM sections WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]
   