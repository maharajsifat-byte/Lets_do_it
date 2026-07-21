import json
import os
class Database:
    def __init__(self):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
        self.files = { 
            "questions": os.path.join(parent_dir, "data", "questions.json"),
            "results": os.path.join(parent_dir, "data", "results.json"),
            "users": os.path.join(parent_dir, "data", "users.json"),
        }
        try : 
            test_file = os.path.join(parent_dir, "test_write.tmp")
            with open(test_file, "w") as f:
             f.write("test")
            