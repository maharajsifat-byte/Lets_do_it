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

        def auth_action():
            users = self.db.load("u")
            u, p = u_ent.get().strip(), p_ent.get().strip()

            if not u or not p:
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            if mode=="login":
                if u in users and users[u]==p:
                    self.current_user = u
                    self.show_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid credentials")
            else:
                if u in users:
                    messagebox.showerror("Error", "Username already exists")
                else:
                    users[u]=p
                    self.db.save("u", users)
                    messagebox.showinfo("Success", "Regitration successful!")
                    self.show_auth_screen("login")

        btn_txt="Sign In" if mode=="login" else "Register"
        StyledButton(card, text=btn_txt, command=auth_action, width=28).pack(pady=(10,15))

        link_txt ="New user? Register here" if mode=="login" else "Already have an account? Sign In"
        link_btn=tk.Button(card, text=link_txt, bg=SIDEBAR_COLOR, fg=ACCENT_COLOR, activebackground=SIDEBAR_COLOR,
                           activeforeground=C_HOVER, bd=0, font=("Seoge UI", 10, "underline"),
                           command=lambda: self.show_auth_screen("register" if mode=="login" else "login"),
                           cursor="hand2")
        link_btn.pack()

    def show_dashboard(self):
        self.clear_screen()

        side=tk.Frame(self.main_container, bg="#020617", width=260)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="UNIVERSITY", font=("Seoge UI", 18, "bold"), fg=ACCENT_COLOR, bg="#020617", pady=30).pack()

        menu=[
             ("🏠  Home", self.welcome_view), 
                        ("📝  Play Quiz", self.quiz_view), 
                        ("⚙️  Question Manager", self.manager_view), 
                        ("🏆  Leaderboard", self.leaderboard_view), 
                        ("📊  Statistics", self.stats_view), 
                        ("💾  Save Local Data", self.save_data_flow),
                        ("📂  Load Local Data", self.load_data_flow),
                        ("🚪  Logout", lambda: self.show_auth_screen("login")),
                        ("❌  Exit", self.root.quit)
        ]

        for t, c in menu:
            btn=tk.Button(side, text=t, font=("Seoge UI", 11, "bold"), bg="#020617", fg="white", bd=0,
                          anchor="w", padx=30, pady=12, command=c, cursor="hand2",
                          activebackground="#1E293B", activeforeground=ACCENT_COLOR)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0F172A", fg=ACCENT_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#020617", fg="white"))

        self.content = tk.Frame(self.main_container, bg=BG_DARK)
        self.content.pack(side="right", expand=True, fill="both")
        self.welcome_view()

    def welcome_view(self):
        for w in self.content.winfo_children():
            w.destroy()

        welcome_frame =tk.Frame(self.content, bg=BG_DARK)
        welcome_frame.pack(expand=True, fill="both")

        tk.Label(welcone_frame, text=f"Welcome Back, {self.current_user}!",
                 font=("Seoge UI", 28, "bold"), bg=BG_DARK, fg=TEXT_WHITE).pack(pady=(220,10))

        tk.Label(welcome_frame, text="Varsity Quiz & Academic Result System",
                 font=("Seoge UI", 12), bg=BG_DARK, fg="grey").pack()