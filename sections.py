from db import db

def new_section(topic):
    sql = "INSERT INTO sections (topic, visible) VALUES (:topic, TRUE) RETURNING id"
    section_id = db.session.execute(sql, {"topic":topic}).fetchone()[0]
    db.session.commit()
    return section_id

def get_topic(section_id):
    id = section_id
    sql = "SELECT topic FROM sections WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

#TODO: käsittele puuttuvat tiedot + PVM muotoilu
def get_sections():
    sql = "SELECT S.id, S.topic, COUNT(DISTINCT (CASE WHEN T.visible THEN T.id END)), COUNT(DISTINCT (CASE WHEN M.visible AND T.visible THEN M.id END)), MAX((CASE WHEN M.visible THEN M.sent_at END)) FROM sections S LEFT JOIN threads T ON S.id = T.section_id LEFT JOIN messages M ON T.id = M.thread_id WHERE S.visible GROUP BY S.id, S.topic"
    result = db.session.execute(sql).fetchall()
    return result

def remove_section(id):
    sql = "UPDATE sections SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
   