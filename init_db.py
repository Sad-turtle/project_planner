import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        port="5433",
        dbname="project_planning",
        user="postgres",
        password="1")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS tasks;')
cur.execute('CREATE TABLE tasks (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'description varchar (255),'
                                 'done boolean,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO tasks (name, description, done)'
            'VALUES (%s, %s, %s)',
            ('Create DB',
             'make 3 tables of sql: users, tasks and projects',
             False)
            )


cur.execute('INSERT INTO tasks (name, description, done)'
            'VALUES (%s, %s, %s)',
            ('Celebrate',
             'Buy smth cool fckng bastard',
             True)
            )

conn.commit()

cur.close()
conn.close()
