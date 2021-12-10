import sqlite3

from pathlib import Path

# Setup paths for database
db_folder = Path('C:/Users/jtate/PycharmProjects/project_manager/db')
db_path = Path.joinpath(db_folder, 'project_manager.db')


# Create Initial Database
project_table = {'id', }



def create_database():
    conn = sqlite3.connect(db_path)
    conn.close()

def create_tables():
    project_table_sql = ('''CREATE TABLE IF NOT EXISTS Projects
                        (ProjectID INT PRIMARY KEY, 
                        Title TEXT, 
                        Description TEXT,
                        Status INT, 
                        Deadline INT, 
                        Priority INT)''')

    task_table_sql = ('''CREATE TABLE IF NOT EXISTS Tasks
                     (TaskID INT PRIMARY KEY,
                      Description TEXT,
                      Deadline INT,
                      CompletionDate INT,
                      Priority INT,
                      ProjectID INT, 
                      FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID))''')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(project_table_sql)
    cursor.execute(task_table_sql)
    conn.commit()
    conn.close()


create_tables()