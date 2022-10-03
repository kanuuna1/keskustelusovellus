CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE sections (
    id SERIAL PRIMARY KEY,
    topic TEXT
    visible BOOLEAN
);    

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    heading TEXT UNIQUE,
    section_id INTEGER REFERENCES sections,
    user_id INTEGER REFERENCES users
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads
    visible BOOLEAN
);

