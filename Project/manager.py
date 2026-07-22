from typing import Any, cast

from database import Database

class QuestionManager:
    def __init__(self):
        self.db = Database()
    def delete_question(self, q_id):
        db = cast(Any, self.db)
        qs = db.load_data(db.q_file)
        qs = [q for q in qs if q['id'] != q_id]
        db.save_data(db.q_file, qs)