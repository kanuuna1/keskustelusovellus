from db import db

def get_all_messages(thread_id):
    sql = "SELECT content FROM messages WHERE thread_id=:thread_id AND visible=TRUE ORDER BY sent_at"
    result = db.session.execute(sql, {"thread_id":thread_id}).fetchall()
    db.session.commit()
    return result

def new_message(content, user_id, thread_id):
    sql = "INSERT INTO messages (content, sent_at, user_id, thread_id, visible) VALUES (:content, NOW(), :user_id, :thread_id, TRUE) RETURNING id"
    message_id = db.session.execute(sql, {"content":content, "thread_id":thread_id, "user_id":user_id}).fetchone()[0]
    db.session.commit()
    return message_id
