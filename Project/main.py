import tkinter as tk 
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import os

from database import Database
from manager import QuestionManager
from stats_engine import StatsEngine
from pdf_parser import PDFProcessor
from gui_components import StyledButton, QuestionFormDialog
from styles import *

class MainApp:
    