import math

import tkinter as tk
from tkcalendar import DateEntry
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from project_manager_db_functions import create_db_engine, date_to_int_conversion
from project_manager_sqlalchemy_classes import Project, Task


# class task frame

# class representing the landing / main control page
class FrontPage:

    def __init__(self, master):
        self.master = master
        self.project_frames = {}  # initialise a container for all active projects
        self.screen_width = None
        self.screen_height = None


    def add_controls(self):
        self.add_project_btn = tk.Button(self.master, text='Add Project', command=lambda: self.add_project())
        self.add_project_btn.grid(row=math.ceil(len(self.project_frames) / 4), column=0)


    def add_project(self):
        pf = ProjectForm(self.master)

    def get_active_projects(self):
        statement = select(Project)
        results = session.execute(statement).scalars().all()
        print(results)
        for i, r in enumerate(results):
            if r:
                self.project_frames[i] = ProjectFrame(self.master, r)

    def layout_projects(self):
        for j, v in enumerate(self.project_frames.values()):
            # these lines look to set the layout of the projects in the window, needs more customising
            grid_row = math.floor(j/4)
            grid_column = j % 4
            v.update_frame()
            v.grid(row=grid_row, column=grid_column, sticky='nsew')  # project frames are placed.

            self.add_project_btn = tk.Button(self.master, text='Add Project', command=lambda: self.add_project())
            self.add_project_btn.grid(row=3, column=0)
        for k in range(3):
            self.master.grid_rowconfigure(k, minsize=self.screen_height / 3, weight=1)
        for m in range(4):
            self.master.grid_columnconfigure(m, minsize=self.screen_width / 4, weight=1)



    def update_page(self):
        self.get_active_projects()
        self.layout_projects()
        self.add_controls()



# each project has its own frame where tasks and controls are held
class ProjectFrame(tk.Frame):

    def __init__(self, master, project):
        super().__init__(master)
        self.project = project
        self.title = tk.Label(self, text=self.project.Title)
        self.title.grid(row=0, column=0)

        self['highlightthickness'] = 1
        self['highlightbackground'] = 'black'

        self.task_frames = []  # list to hold all tasks in the project
        self.new_task_var = tk.StringVar()
        self.new_task_entry = tk.Entry(self, textvariable=self.new_task_var)
        self.new_task_entry.grid(row=1, column=0)

        self.add_task_btn = tk.Button(self, text='Add Task', command=self.add_task)
        self.add_task_btn.grid(row=1, column=1)
        self.populate_tasks()

    def add_task(self):
        newTask = Task(Description=self.new_task_var.get(),
                       Deadline=20221111,
                       CompletionDate=20221212,
                       Priority=1,
                       projectid=self.project.id)

        session.add(newTask)
        session.flush()
        session.commit()
        self.new_task_var.set("")
        self.populate_tasks()
        self.layout_tasks()

    def populate_tasks(self):
        for r in self.project.Tasks:
            self.task_frames.append(TaskFrame(self, r))

    def layout_tasks(self):
        for i, t in enumerate(self.task_frames, 2):
            t.grid(row=i, column=0)

    def update_frame(self):
        for tf in self.task_frames:
            print(tf)
            tf.destroy()
        self.populate_tasks()
        self.layout_tasks()

# class for new project entry
class ProjectForm:

    def __init__(self, master):
        self.entry_window = tk.Toplevel(master)

        self.p = None
        self.frame_width = None
        self.frame_height = None
        self.date_integer = None

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
        self.p = Project(id=None,
                         Title=self.title_var.get(),
                         Description=self.description_var.get(),
                         Status=self.status_var,
                         Priority=self.priority_var,
                         Deadline=self.date_integer)

        session.add(self.p)
        session.flush()
        print(self.p.id)
        session.commit()

        self.entry_window.destroy()
        front_page.add_project_btn.destroy()
        front_page.update_page()


# frame to hold task details and controls
class TaskFrame(tk.Frame):

    def __init__(self, master, task):
        super().__init__(master)
        self.task_description = tk.Label(self, text=task.Description)
        self.task_description.pack()


def main():

    root = tk.Tk()
    global front_page
    front_page = FrontPage(root)
    front_page.screen_width = root.winfo_screenwidth()
    front_page.screen_height = root.winfo_screenheight()
    front_page.update_page()
    root.geometry(f'{front_page.screen_width}x{front_page.screen_height}')

    root.mainloop()


if __name__ == "__main__":
    engine = create_db_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session(future=True)
    main()




