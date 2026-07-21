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
            os.remove(test_file)
        except Exception:
            self.files = {
                "questions": os.path.join(base_dir, "questions.json"),
                "results": os.path.join(base_dir, "results.json"),
                "users": os.path.join(base_dir, "users.json")
            }
             self.initialize()

    def initialize(self):
       for key, path in self.files.items():
          if not os.path.exists(path):
             if key == "u":
                    default = {"admin": "123"}
                elif key == "q":
                    default = [
                        {
                            "id": 0,
                            "question": "According to 2023 global statistics, what is Bangladesh's rank in Rice production?",
                            "options": ["A) 1st Position", "B) 2nd Position", "C) 3rd Position", "D) 4th Position"],
                            "answer": "C) 3rd Position"
                        },