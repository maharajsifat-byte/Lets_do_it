import tkinter as tk
from tkinter import ttk, messagebox
from styles import *

class StyledButton(tk.Button):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent, text=text, command=command,
            bg=ACCENT_COLOR, fg=BG_DARK,
            activebackground=C_HOVER, activeforeground=BG_DARK,
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
    def setup_ui(self):
        main_frame = tk.Frame(self, bg=BG_DARK, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="Question text:", bg=BG_DARK, fg=TEXT_WHITE, font=FONT_REG).pack(anchor="w", pady=(0, 5))
        self.q_text = tk.Text(main_frame, height=4, width=50, font=FONT_REG, bg=SIDEBAR_COLOR, fg=TEXT_WHITE, bd=0)
        self.q_text.pack(fill="x", pady=(0, 15))
        self.opt_entries = []

        for i in range(4):
            tk.Label(main_frame, text=f"Option {chr(65+i)}:", bg=BG_DARK, fg=TEXT_WHITE, font=FONT_REG).pack(anchor="w", pady=(0, 2))
            ent = tk.Entry(main_frame, font=FONT_REG, bg=SIDEBAR_COLOR, fg=TEXT_WHITE, bd=0)
            ent.pack(fill="x", pady=(0, 10))
            self.opt_entries.append(ent)
            tk.Label(main_frame, text="Correct Option (A, B, C, or D):", bg=BG_DARK, fg=TEXT_WHITE, font=FONT_REG).pack(anchor="w", pady=(0, 2))
        self.ans_entry = tk.Entry(main_frame, font=FONT_REG, bg=SIDEBAR_COLOR, fg=TEXT_WHITE, bd=0)
        self.ans_entry.pack(fill="x", pady=(0, 20))

        if self.initial_data:
            self.q_text.insert("1.0", self.initial_data["question"])
            for i, opt in enumerate(self.initial_data["options"]):
                clean_opt = opt[3:].strip() if opt.startswith(("A)", "B)", "C)", "D)")) else opt
                self.opt_entries[i].insert(0, clean_opt)
            
            ans_val = self.initial_data["answer"]
            clean_ans = ans_val[0] if ans_val and ans_val[1:3] == ") " else ans_val
            self.ans_entry.insert(0, clean_ans)

        StyledButton(main_frame, text="Save Question", command=self.save_action).pack(anchor="e")

