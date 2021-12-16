import tkinter as tk
from tkcalendar import Calendar, DateEntry

from project_manager_db_functions import create_session
from project_manager_sqlalchemy_classes import Project, Task
# class project frame
# class task frame
# class control frame
# class project form

session = None


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


        self.add_to_db_btn = tk.Button(self.entry_window, text='Add Project', command=self.add_to_db)
        self.add_to_db_btn.grid(row=len(self.label_list)+1, column=0)



    def add_to_db(self):
        self.p = Project(title=self.title_var,
                         description=self.description_var,
                         status=self.status_var,
                         priority=self.priority_var,
                         deadline=self.deadline)
        session.add(self.p)
        session.commit()

def add_project(master):

    pf = ProjectForm(master)

def main():

    root = tk.Tk()
    Session = create_session()
    session = Session()

    add_project_btn = tk.Button(root, command=add_project(root))
    add_project_btn.pack()

    root.mainloop()


if __name__ == "__main__":
    main()





