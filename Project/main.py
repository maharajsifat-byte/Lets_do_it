import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime 
import os

from database import Database
from manager import QuestionManager
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
        tk.Label(card, text=title_text, font=("Segoe UI", 22,"bold"), bg=SIDEBAR_COLOR, fg=ACCENT_COLOR).pack(pady=(10, 5))

        subtitle = "Access quix engine & analytics" if mode== "login" else "Join the academic quiz dashboard"
        tk.Label(card, text=subtitle, font=("Segoe UI", 10), bg=SIDEBAR_COLOR, fg="grey").pack(pady=(0,25))

        tk.Label(card, text="Username", font=("Segoe UI", 10, "bold"), bg=SIDEBAR_COLOR, fg=TEXT_WHITE).pack(anchor="w", pady=(5,2))
        u_ent = ttk.Entry(card, width=35, font=("Segoe UI", 11))
        u_ent.pack(pady=(0,15))

        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"), bg=SIDEBAR_COLOR, fg=TEXT_WHITE).pack(anchor="w", pady=(5,2))
        p_ent = ttk.Entry(card, width=35, show="*", font=("Segoe UI", 11))
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
                           activeforeground=C_HOVER, bd=0, font=("Segoe UI", 10, "underline"),
                           command=lambda: self.show_auth_screen("register" if mode=="login" else "login"),
                           cursor="hand2")
        link_btn.pack()

    def show_dashboard(self):
        self.clear_screen()

        side=tk.Frame(self.main_container, bg="#020617", width=260)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="UNIVERSITY", font=("Segoe UI", 18, "bold"), fg=ACCENT_COLOR, bg="#020617", pady=30).pack()

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
            btn=tk.Button(side, text=t, font=("Segoe UI", 11, "bold"), bg="#020617", fg="white", bd=0,
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

        tk.Label(welcome_frame, text=f"Welcome Back, {self.current_user}!",
                 font=("Segoe UI", 28, "bold"), bg=BG_DARK, fg=TEXT_WHITE).pack(pady=(220,10))

        tk.Label(welcome_frame, text="Varsity Quiz & Academic Result System",
                 font=("Segoe UI", 12), bg=BG_DARK, fg="grey").pack()

    def quiz_view(self):
        self.quiz_data=self.db.load("q")
        if not self.quiz_data:
            return messagebox.showwarning("Empty Bank", "No questions available. Please add some questions first.")
        self.q_idx=0
        self.score=0
        self.render_q()

    def render_q(self):
        for w in self.content.winfo_children():
            w.destroy()

        q=self.quiz_data[self.q_idx]

        progress_frame=tk.Frame(self.content, bg=BG_DARK)
        progress_frame.pack(pady=(40,0), padx=50, fill="x")

        tk.Label(progress_frame, text=f"Question {self.q_idx+1} of {len(self.quiz_data)}",
                 font=("Segoe UI", 10, "bold"), bg=BG_DARK, fg=ACCENT_COLOR).pack(side="left")

        card=tk.Frame(self.content, bg=CARD_BG, padx=40, pady=40)
        card.pack(pady=20, padx=50, fill="both", expand=True)

        tk.Label(card, text=q['question'], font=("Segoe UI", 15, "bold"), bg=CARD_BG, fg=TEXT_WHITE, wraplength=700, justify="left").pack(anchor="w", pady=(0,25))

        self.selected_option=tk.StringVar(value="")
        for o in q['options']:
            rb_frame=tk.Frame(card, bg=CARD_BG)
            rb_frame.pack(anchor="w", fill="x", pady=5)

            rb=tk.Radiobutton(rb_frame, text=o, variable=self.selected_option, value=o,bg=CARD_BG, fg=TEXT_WHITE,
                             selectcolor=BG_DARK, activebackground=CARD_BG, activeforeground=ACCENT_COLOR, font=("Segoe UI", 11),cursor="hand2")
            rb.pack(anchor="w", padx=10, pady=5)

        btn_frame=tk.Frame(self.content, bg=BG_DARK)
        btn_frame.pack(pady=(0,40), fill="x", padx=50)

        StyledButton(btn_frame, text="SUBMIT & NEXT ➔", command=self.submit_answer).pack(side="right")

    def submit_answer(self):
        if not self.selected_option.get():
            messagebox.showwarning("Selection Required", "PLease select an option to proceed.")
            return

        if self.selected_option.get() == self.quiz_data[self.q_idx]['answer']: 
                    self.score += 1

        self.q_idx +=1
        if self.q_idx < len(self.quiz_data):
            self.render_q()
        else:
            res=self.db.load("r")
            res.append({
                "name": self.current_user,
                "score": self.score,
                "total": len(self.quiz_data),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.db.save("r",res)

            percentage= (self.score / len(self.quiz_data))*100
            feedback = "excellent performance!" if percentage >= 80 else "Good job! Keep practicing." if percentage >= 50 else "Keep studying and try again!"

            messagebox.showinfo("Quiz Completed", f"Quiz Over!\n\nYour Score: {self.score}/{len(self.quiz_data)}({percentage:.1f}%)\n\n{feedback}")
            self.welcome_view()

    def manager_view(self):
            for w in self.content.winfo_children(): 
                w.destroy()
    
            manager_frame = tk.Frame(self.content, bg=BG_DARK, padx=30, pady=30)
            manager_frame.pack(fill="both", expand=True)
    
            header_frame = tk.Frame(manager_frame, bg=BG_DARK)
            header_frame.pack(fill="x", pady=(0, 20))
    
            tk.Label(header_frame, text="QUESTION MANAGER", font=("Segoe UI", 18, "bold"), bg=BG_DARK, fg=TEXT_WHITE).pack(side="left")
    
            controls_frame = tk.Frame(manager_frame, bg=BG_DARK)
            controls_frame.pack(fill="x", pady=(0, 15))
    
            self.search_ent = ttk.Entry(controls_frame, width=30, font=FONT_REG)
            self.search_ent.pack(side="left", padx=(0, 10))
    
            StyledButton(controls_frame, text="Search", command=self.search_flow).pack(side="left", padx=5)
            StyledButton(controls_frame, text="Add Question", command=self.add_q_flow).pack(side="left", padx=5)
            StyledButton(controls_frame, text="Import PDF", command=self.import_pdf_flow).pack(side="left", padx=5)

            list_frame=tk.Frame(manager_frame, bg=SIDEBAR_COLOR)
            list_frame.pack(fill="both", expand=True)

            self.tree=ttk.Treeview(list_frame, columns=("id","text","ans"), show="headings", selectmode="browse")
            self.tree.heading("id", text="ID")
            self.tree.heading("text", text="Question Text")
            self.tree.heading("ans",text="Correct Answer")

            self.tree.column("id", width=50, anchor="center")
            self.tree.column("text", width=500, anchor="w")
            self.tree.column("ans", width=180, anchor="center")

            self.tree.pack(side="left", fill="both", expand=True)

            scroller=ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
            scroller.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=scroller.set)

            actions_frame=tk.Frame(manager_frame, bg=BG_DARK)
            actions_frame.pack(fill="x", pady=(15,0))

            StyledButton(actions_frame, text="Update Selected", command=self.update_q_flow).pack(side="left", padx=(0,10))
            StyledButton(actions_frame, text="Delete Selected", command=self.delete_q_flow).pack(side="left")

            self.load_tree_data()

    def load_tree_data(self, dataset=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        qs=dataset if dataset is not None else self.manager.get_all_questions()
        for q in qs:
            self.tree.insert("", "end", values=(q['id'], q['question'], q['answer']))
    def search_flow(self):
        term=self.search_ent.get().strip()
        results=self.manager.search_questions(term)
        self.load_tree_data(results)

    def add_q_flow(self):
        def on_save(q_text, opts, ans):
            self.manager.add_question(q_text, opts, ans)
            self.load_tree_data()
            messagebox.showinfo("Success", "Question added successfully!")

        QuestionFormDialog(self.root, "Add New Question", on_save)
        