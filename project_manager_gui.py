import math
import datetime

import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from sqlalchemy import select, delete
from sqlalchemy.orm import sessionmaker

from project_manager_db_functions import create_db_engine, date_to_int_conversion, int_to_date_conversion
from project_manager_sqlalchemy_classes import Project, Task
import project_manager_styling as pms


# class representing the landing / main control page
class FrontPage:

    def __init__(self, master):
        self.master = master
        self.master.title("Project Manager")
        self.project_frames = {}  # initialise a container for all active projects
        self.styling = pms.ProjectFonts()
        # configs
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.master.geometry(f'{self.screen_width}x{self.screen_height}')
        self.master.grid_propagate(0)

        # set menu controls
        self.add_controls()
        self.master.config(menu=self.menubar)




    def add_controls(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Add Project', command=self.add_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='View Project History', command=self.view_project_history)
        self.menubar.add_cascade(label='File', menu=self.filemenu)


    def add_project(self):
        pf = ProjectForm(self.master)

    def view_project_history(self):
        ph = ProjectHistory(self.master)

    def get_active_projects(self):
        statement = select(Project)
        results = session.execute(statement).scalars().all()
        self.project_frames = {}
        for i, r in enumerate(results):
            if r:
                if r.Status == 0:
                    newpf = ProjectFrame(self.master, r)
                    self.project_frames[i] = newpf

    def layout_projects(self):
        for j, v in enumerate(self.project_frames.values()):
            # these lines look to set the layout of the projects in the window, needs more customising
            grid_row = math.floor(j/4)
            grid_column = j % 3
            v.grid(row=grid_row, column=grid_column, sticky='nsew', padx=10, pady=10)  # project frames are placed.

        for k in range(2):
            self.master.grid_rowconfigure(k, minsize=self.screen_height / 2, weight=1)
        for m in range(4):
            self.master.grid_columnconfigure(m, minsize=self.screen_width / 4, weight=1)


    def update_page(self):
        self.get_active_projects()
        self.layout_projects()

    def update_session(self):
        session.commit()
        session.flush()
        self.update_page()

# each project has its own frame where tasks and controls are held
class ProjectFrame(tk.Frame):

    def __init__(self, master, project):
        super().__init__(master)
        self.project = project

        # frames setup for controls and tasks
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=0, column=0, padx=5, pady=5, sticky='news')


        self.task_holder_frame = tk.Frame(self)
        self.task_holder_frame.grid(row=1, column=0, pady=5, padx=5, sticky='news')


        # configurations
        self['highlightthickness'] = 5
        self['highlightbackground'] = 'black'
        self.grid_rowconfigure(0, weight=1, uniform='x')
        self.grid_rowconfigure(1, weight=3, uniform='x')


        #  column weightings for the control frame
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=4)
        self.control_frame.grid_columnconfigure(2, weight=4)
        self.control_frame.grid_columnconfigure(3, weight=2)
        self.control_frame.grid_columnconfigure(4, weight=2)

        #  row weightings
        self.control_frame.grid_rowconfigure(0, weight=1)
        self.control_frame.grid_rowconfigure(1, weight=1)
        self.control_frame.grid_rowconfigure(2, weight=2)
        self.control_frame.grid_rowconfigure(3, weight=2)
        self.control_frame.grid_rowconfigure(4, weight=2)

        # control frame populated
        self.title = tk.Label(self.control_frame, text=self.project.Title, font=front_page.styling.projectfont)
        self.title.grid(row=0, column=0, columnspan=3, rowspan=2, pady=5, sticky='ew')

        self.deadline_label = tk.Label(self.control_frame,
                                       text="Project Deadline",
                                       font=front_page.styling.datefont)
        self.deadline_label.grid(row=0, column=3, columnspan=2, sticky='s')
        self.deadline_int = self.project.Deadline
        self.deadline_date = int_to_date_conversion(self.deadline_int)
        self.deadline = tk.Label(self.control_frame,
                                 text=self.deadline_date.strftime("%x"),
                                 font=front_page.styling.datefont)
        self.deadline.grid(row=1, column=3, columnspan=2, sticky='n')

        self.description = tk.Label(self.control_frame,
                                    text=self.project.Description,
                                    font=front_page.styling.projdescriptionfont)
        self.description.grid(row=2, column=0, columnspan=3, pady=5)

        # project control buttons
        self.complete_project_btn = tk.Button(self.control_frame, text='Complete Project',
                                              command=self.complete_project,
                                              font=front_page.styling.buttonfont)
        self.complete_project_btn.grid(row=3, column=1)

        self.delete_project_btn = tk.Button(self.control_frame, text='Delete Project',
                                            command=self.delete_project,
                                            font=front_page.styling.buttonfont)
        self.delete_project_btn.grid(row=3, column=2)

        self.view_project_archive_btn = tk.Button(self.control_frame, text='View Archive',
                                                  command=self.view_project_archive,
                                                  font=front_page.styling.buttonfont)
        self.view_project_archive_btn.grid(row=3, column=4)

        # new task labels and controls

        self.new_task_var = tk.StringVar()
        self.new_task_entry = tk.Entry(self.control_frame, textvariable=self.new_task_var)
        self.new_task_entry.grid(row=4, column=0, columnspan=2, sticky='sew', padx=5, pady=5)

        self.new_task_date = self.deadline = DateEntry(self.control_frame)
        self.new_task_date.grid(row=4, column=2)


        self.add_task_btn = tk.Button(self.control_frame,
                                      text='Add Task',
                                      command=self.add_task,
                                      font=front_page.styling.buttonfont)
        self.add_task_btn.grid(row=4, column=4)


        # scrollbar

        self.task_scrollbar = tk.Scrollbar(self.task_holder_frame, orient='vertical')
        self.task_scrollbar.grid(row=0, column=3)

        self.task_frames = []  # list to hold all tasks in the project
        self.task_labels = []  # holds numerical labels in memory
        self.populate_tasks()
        self.layout_tasks()

    def add_task(self):
        deadline_raw = self.new_task_date.get_date()
        newTask = Task(Description=self.new_task_var.get(),
                       Deadline=date_to_int_conversion(deadline_raw),
                       CompletionDate=0,
                       Status=0,
                       projectid=self.project.id)

        session.add(newTask)

        self.new_task_var.set("")
        front_page.update_session()

    def populate_tasks(self):

        def sort_date(taskframe):
            return taskframe.task.Deadline

        self.task_frames = []
        for r in self.project.Tasks:
            if r.Status == 0:
                self.task_frames.append(TaskFrame(self.task_holder_frame, r))
        self.task_frames.sort(key=sort_date)


    def layout_tasks(self):
        self.task_labels = []
        for i, t in enumerate(self.task_frames, 0):
            task_label = tk.Label(self.task_holder_frame,
                                  text=i+1,
                                  font=front_page.styling.taskfont)
            self.task_labels.append(task_label)
            task_label.grid(row=i, column=0, sticky='w')
            t.grid(row=i, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
            self.task_holder_frame.grid_rowconfigure(i, weight=1, uniform='y')
        self.task_holder_frame.columnconfigure(0, weight=1)
        self.task_holder_frame.columnconfigure(1, weight=8)
        self.task_holder_frame.columnconfigure(2, weight=1)
    def complete_project(self):
        res = messagebox.askyesno('Warning', 'Complete Project & Archive?')
        if res == True:
            self.project.Status = 1
            self.project.CompletionDate = date_to_int_conversion(datetime.date.today())
            session.add(self.project)
            self.destroy()
        front_page.update_session()

    def delete_project(self):
        res = messagebox.askyesno('Warning', 'Delete Project?')
        if res == True:
            statement = delete(Project).where(Project.id == self.project.id)
            session.execute(statement)
            self.destroy()
        front_page.update_session()

    def view_project_archive(self):
        newArchiveWindow = Archive(self.master, self.project)


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

        self.status_var = 0
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
                         CompletionDate=0,
                         Priority=self.priority_var,
                         Deadline=self.date_integer)

        session.add(self.p)
        self.entry_window.destroy()
        front_page.update_session()


# frame to hold task details and controls
class TaskFrame(tk.Frame):

    def __init__(self, master, task):
        super().__init__(master)
        self.task = task
        #  configuration
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self['highlightthickness'] = 2
        self['highlightbackground'] = 'black'

        self.task_description = tk.Label(self, text=self.task.Description, font=front_page.styling.taskfont)
        self.task_description.grid(row=0, column=0, sticky='ew')

        self.task_deadline = tk.Label(self, text=int_to_date_conversion(self.task.Deadline), font=front_page.styling.datefont)
        self.task_deadline.grid(row=0, column=1, sticky='e')

        self.complete_task_btn = tk.Button(self, text=u'\u2713', command = self.complete_task,)
        self.complete_task_btn.grid(row=0, column=2, sticky='e')

        self.delete_task_btn = tk.Button(self, text="X", command = self.delete_task)
        self.delete_task_btn.grid(row=0, column=3,sticky='e')

    def delete_task(self):
        statement = delete(Task).where(Task.id == self.task.id)
        session.execute(statement)
        front_page.update_session()

    def complete_task(self):
        self.task.Status = 1
        self.task.CompletionDate = date_to_int_conversion(datetime.date.today())
        session.add(self.task)
        front_page.update_session()

class Archive(tk.Toplevel):

    def __init__(self, master, project):
        super().__init__(master)
        self.project = project

        self.title_label = tk.Label(self, text=self.project.Title, font=front_page.styling.taskfont)
        self.title_label.grid(row=0, column=0, pady=5, padx=5)

        self.task_header_label = tk.Label(self, text='Task', font=front_page.styling.taskfont)
        self.task_header_label.grid(row=1, column=0, pady=5, padx=5)

        self.deadline_header_label = tk.Label(self, text='Deadline', font=front_page.styling.taskfont)
        self.deadline_header_label.grid(row=1, column=1, pady=5, padx=5)

        self.completed_header_label = tk.Label(self, text='Completed', font=front_page.styling.taskfont)
        self.completed_header_label.grid(row=1, column=2, pady=5, padx=5)

        sorted_tasks = [i for i in self.project.Tasks]
        sorted_tasks.sort(key=lambda y: (y.Deadline, y.CompletionDate))

        for i, r in enumerate(sorted_tasks, 2):
            descrip_text = r.Description
            deadline_text = int_to_date_conversion(r.Deadline)
            if r.Status == 1:
                self.descrip_value = tk.Label(self, text=descrip_text, font=front_page.styling.comptaskfont)
                completion_text = int_to_date_conversion(r.CompletionDate)
            else:
                self.descrip_value = tk.Label(self, text=descrip_text, font=front_page.styling.taskfont)
                completion_text = ""

            self.descrip_value = tk.Label(self, text=descrip_text, font=front_page.styling.taskfont)
            self.descrip_value.grid(row=i, column=0, padx=5, pady=5)

            self.deadline_value = tk.Label(self, text=deadline_text, font=front_page.styling.taskfont)
            self.deadline_value.grid(row=i, column=1, padx=5, pady=5)

            self.completion_value = tk.Label(self, text=completion_text, font=front_page.styling.taskfont)
            self.completion_value.grid(row=i, column=2, padx=5, pady=5)

        self.exit_archive_btn = tk.Button(self, text='Exit', command=self.exit_archive, font=front_page.styling.buttonfont)
        self.exit_archive_btn.grid(row=0, column=1)

    def exit_archive(self):
        self.destroy()


# Class for the project history
class ProjectHistory(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        statement = select(Project)
        self.results = session.execute(statement).scalars().all()
        print(self.results)

        self.header = tk.Label(self, text='Project History', font=front_page.styling.projectfont)
        self.header.grid(row=0, column=0, columnspan=4)

        self.title_header = tk.Label(self, text='Title', font=front_page.styling.smallheadfont)
        self.title_header.grid(row=1, column=0)

        self.status_header = tk.Label(self, text='Status', font=front_page.styling.smallheadfont)
        self.status_header.grid(row=1, column=1)

        self.deadline_header = tk.Label(self, text='Deadline', font=front_page.styling.smallheadfont)
        self.deadline_header.grid(row=1, column=2)

        self.completed_header = tk.Label(self, text='Completed', font=front_page.styling.smallheadfont)
        self.completed_header.grid(row=1, column=3)

        self.set_results()

    def set_results(self):

        self.history_dic = {}
        for i, proj in enumerate(self.results, 2):
            new_rec = HistoryRecord(self, proj, i)
            self.history_dic[i] = new_rec



class HistoryRecord:

    def __init__(self, master, proj, start_row):
        self.project = proj
        self.master= master

        proj_btn = tk.Button(self.master, text=proj.Title, command=self.view_archive,
                             font=front_page.styling.taskfont)
        status_text = 'Active'
        comp_date = ''

        if proj.Status == 1:
            status_text = 'Complete'
            comp_date = int_to_date_conversion(proj.CompletionDate)

        status_lbl = tk.Label(self.master, text=status_text, font=front_page.styling.taskfont)
        deadline_lbl = tk.Label(self.master, text=int_to_date_conversion(proj.Deadline), font=front_page.styling.datefont)
        complete_lbl = tk.Label(self.master, text=comp_date, font=front_page.styling.datefont)

        proj_btn.grid(row=start_row, column=0)
        status_lbl.grid(row=start_row, column=1)
        deadline_lbl.grid(row=start_row, column=2)
        complete_lbl.grid(row=start_row, column=3)

    def view_archive(self):
        nA = Archive(self.master, self.project)


def main():

    root = tk.Tk()
    global front_page
    front_page = FrontPage(root)
    front_page.update_page()
    root.mainloop()


if __name__ == "__main__":
    engine = create_db_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session(future=True)
    main()




