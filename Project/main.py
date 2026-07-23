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