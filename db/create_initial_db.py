import sqlite3

from pathlib import Path

# Setup paths for database
db_folder = Path('C:/Users/jtate/PycharmProjects/project_manager/db')
db_path = Path.joinpath(db_folder, 'project_manager.db')


# Create Initial Database

def create_database():
    conn = sqlite3.connect(db_path)
    conn.close()

def create_tables():
    project_table_sql = ('''CREATE TABLE IF NOT EXISTS Projects
                        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , 
                        Title TEXT, 
                        Description TEXT,
                        Status INTEGER, 
                        CompletionDate INTEGER,
                        Deadline INTEGER, 
                        Priority INTERGER)''')

    task_table_sql = ('''CREATE TABLE IF NOT EXISTS Tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      Description TEXT,
                      Deadline INT,
                      Status INTEGER,
                      CompletionDate INT,
                      projectid INT, 
                      FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID) ON DELETE CASCADE)''')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(project_table_sql)
    cursor.execute(task_table_sql)
    conn.commit()
    conn.close()

create_database()
create_tables()