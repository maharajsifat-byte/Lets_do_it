import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime 
import os

from database import Database
from manager import Manager
from stats_engine import StatsEngine
from pdf_parser import PDFparser 
from gui_components import StyledButton, QuestionFormDialog
from styles import *

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Varsity Quiz System Pro")
        self.root.geometry("1150x780")
        self.root.configure(bg=BG_DARK)

        self.db = Database()
        self.manager = QuestionManager()
        self.current_user = None

        self. main_container = tk.Frame(self.root, bg= BG_DARK)
        self.main_container.pack(fill="both", expand=True)

        self.show_auth_screen()

    def clear_screen(self):
        for w in self.main_container.winfo_children():
            w.destroy()

    def show_auth_screen(self,mode="login"):
        self.clear_screen()

        card = tk.Frame(self.main_container, bg=SIDEBAR_COLOR, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        title_text = "STUDENT LOGIN" if mode == "login" else "CREATE ACCOUNT"
        tk.Label(card, text=title_text, font=("Seoge UI", 22,"bold"), bg=SIDEBAR_COLOR, fg=ACCENT_COLOR).pack(pady=(10, 5))

        subtitle = "Access quix engine & analytics" if mode== "login" else "Join the academic quiz dashboard"
        tk.Label(card, text=subtitle, font=("Seoge UI", 10), bg=SIDEBAR_COLOR, fg="grey").pack(pady=(0,25))

        tk.Label(card, text="Username", font=("Seoge UI", 10, "bold"), bg=SIDEBAR_COLOR, fg=TEXT_WHITE).pack(anchor="W", pady=(5,2))
        u_ent = ttk.Entry(card, width=35, font=("Seoge UI", 11))
        u_ent.pack(pady=(0,15))

        tk.Label(card, text="Password", font=("Seoge UI", 10, "bold"), bg=SIDEBAR_COLOR, fg=TEXT_WHITE).pack(anchor="w", pady=(5,2))
        p_ent = ttk.Entry(card, width=35, show="*", font=("Seoge UI", 11))
        p_ent.pack(pady=(0,15))