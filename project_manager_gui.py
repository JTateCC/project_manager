import math

import tkinter as tk
from tkcalendar import DateEntry
from sqlalchemy.orm import sessionmaker

=
from project_manager_db_functions import create_db_engine, date_to_int_conversion
from project_manager_sqlalchemy_classes import Project, Task


# class task frame

# class representing the landing / main control page
class FrontPage:

    def __init__(self, master):
        self.master = master
        self.project_frames = {}  # initialise a container for all active projects
        self.update_page()


    def add_controls(self):
        self.add_project_btn = tk.Button(self.master, text='Add Project', command=lambda: self.add_project())
        self.add_project_btn.grid(row=math.ceil(len(self.project_frames) / 4), column=0)


    def add_project(self):
        pf = ProjectForm(self.master)

    def get_active_projects(self):


        results = session.query(Project).all()
        for i, r in enumerate(results):
            print(r)
            if r:
                self.project_frames[i] = ProjectFrame(self.master, r)

    def layout_projects(self):
        for j, v in enumerate(self.project_frames.values()):
            # these lines look to set the layout of the projects in the window, needs more customising
            grid_row = math.floor(j/5)
            grid_column = j % 4
            v.grid(row=grid_row, column=grid_column)  # project frames are placed.

            self.add_project_btn = tk.Button(self.master, text='Add Project', command=lambda: self.add_project())
            self.add_project_btn.grid(row=math.ceil(len(self.project_frames) / 4), column=0)

    def update_page(self):
        self.get_active_projects()
        self.layout_projects()
        self.add_controls()


# each project has its own frame where tasks and controls are held
class ProjectFrame(tk.Frame):

    def __init__(self, master, project):
        super().__init__(master)
        self.project = project
        self.title = tk.Label(self, self.project.Title)
        self.title.grid(row=0, column=0)


class ProjectForm:

    def __init__(self, master):
        self.entry_window = tk.Toplevel(master)
        self.p = None

        self.title_label = tk.Label(self.entry_window, text='Title')
        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(self.entry_window, textvariable=self.title_var)

        self.description_label = tk.Label(self.entry_window, text='Description')
        self.description_var = tk.StringVar()
        self.description_entry = tk.Entry(self.entry_window, textvariable=self.description_var)

        self.status_var = 1
        self.priority_var = 1

        self.deadline_label = tk.Label(self.entry_window, text='Deadline')
        self.deadline = DateEntry(self.entry_window)

        self.label_list = [self.title_label, self.description_label,self.deadline_label]
        self.entry_list = [self.title_entry, self.description_entry, self.deadline]


        for i, v in enumerate(self.label_list):
            v.grid(row=i, column=0)
            self.entry_list[i].grid(row=i, column=1)


        self.add_to_db_btn = tk.Button(self.entry_window, text='Add Project', command=lambda: self.add_to_db())
        self.add_to_db_btn.grid(row=len(self.label_list)+1, column=0)



    def add_to_db(self):

        self.date_integer = date_to_int_conversion(self.deadline.get_date())
        self.p = Project(Title=self.title_var.get(),
                         Description=self.description_var.get(),
                         Status=self.status_var,
                         Priority=self.priority_var,
                         Deadline=self.date_integer)

        session.add(self.p)
        session.commit()

        self.entry_window.destroy()
        front_page.update_page()


def main():

    root = tk.Tk()

    global front_page
    front_page = FrontPage(root)
    root.mainloop()


if __name__ == "__main__":
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()





