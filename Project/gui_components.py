import tkinter as tk 
from tkinter import ttk , messagebox
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