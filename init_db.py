import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        port="5433",
        dbname="project_planning",
        user="postgres",
        password="1")


cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS "user" CASCADE;')
cur.execute('DROP TABLE IF EXISTS dashboard CASCADE;')
cur.execute('DROP TABLE IF EXISTS project CASCADE;')
cur.execute('DROP TABLE IF EXISTS task CASCADE;')
cur.execute('''
    CREATE TABLE IF NOT EXISTS "user" (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS dashboard (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES "user" (id)
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS project (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        dashboard_id INTEGER NOT NULL,
        FOREIGN KEY (dashboard_id) REFERENCES dashboard (id)
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS task (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        done BOOLEAN DEFAULT FALSE,
        project_id INTEGER NOT NULL,
        FOREIGN KEY (project_id) REFERENCES project (id)
    )
''')


conn.commit()
cur.close()
conn.close()
