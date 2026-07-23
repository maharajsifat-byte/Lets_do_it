import tkinter as tk 
from tkinter import ttk , messagebox
from turtle import title
from styles import *
class StyledButton(tk.Button):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            bg=ACCENT_COLOR, fg=BG_DARK,
            activebackground=C_HOVER_COLOR, activeforeground=BG_DARK,
            font=FONT_REG, bd=0, cursor="hand2", padx=15, pady=8, **kwargs
        )
        class StyledEntry(ttk.Entry):
            def __init__(self, parent, **kwargs):
              super().__init__(parent, font=FONT_REG, **kwargs)

        class QuestionFormDialog(tk.Toplevel):
           def __init__(self, parent, title, on_save, initial_data=None):
             super().__init__(parent)
             self.title(title)
             self.geometry("500x550")
             self.configure(bg=BG_DARK)
             self.on_save = on_save
             self.initial_data = initial_data
             self.setup_ui()
