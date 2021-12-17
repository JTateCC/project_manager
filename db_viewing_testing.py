import sqlite3
from pathlib import Path

# Setup paths for database
db_folder = Path('C:/Users/jtate/PycharmProjects/project_manager/db')
db_path = Path.joinpath(db_folder, 'project_manager.db')

def connect_sqlite():
    conn = sqlite3.connect(db_path)
    return conn

def view_all_projects():

    conn = connect_sqlite()
    c = conn.cursor()
    c.execute('SELECT * FROM Projects')
    projects = c.fetchall()
    print(projects)
    conn.close()

def view_tables():
    conn = connect_sqlite()
    sql_query = """SELECT name FROM sqlite_master 
        WHERE type='table';"""
    c = conn.cursor()
    c.execute(sql_query)
    tables = c.fetchall()
    print(tables)
    conn.close()

def delete_all_projects():
    conn = connect_sqlite()
    c = conn.cursor()
    c.execute('DELETE FROM Projects')
    conn.commit()
    conn.close()

view_all_projects()
#delete_all_projects()
#view_tables()