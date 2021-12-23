import tkinter as tk
import tkinter.font as f

class ProjectFonts:

    def __init__(self):
        self.taskfont = f.Font(family='Times', size=8)
        self.datefont = f.Font(family='Times', size=6, slant='italic')
        self.projectfont = f.Font(family='Times', size=16, weight='bold')
        self.projdescriptionfont = f.Font(family='Times', size=12, slant='italic')
        self.buttonfont = f.Font(family='Times', size=8, weight='bold')

