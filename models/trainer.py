from models.user import User
from data_work.info_add import add_workout_day_to_json
from data_work.info_add import add_attendance_day_to_json
import json

class Trainer(User):
    def __init__(self, username):
        super().__init__(username, "trainer")
        self.specializations = []
        self.sessions = []

    def assign_workout(self, username, date, workout):
        return add_workout_day_to_json(username, date, workout)

    def add_attendance_day(self, username, date):
        return add_attendance_day_to_json(username, date)
    
    def attendance_tracking(self, username):
        #return attendance_tracking_data(username)
        pass

    def get_trainer_info(username):
        with open("data/trainer_info.json", "r", encoding="utf-8") as f:
            trainers = json.load(f)
        for t in trainers:
            if t["username"] == username:
                return t
        return None
    
    def get_trainer_phone(self):
        trainer_info = self.get_trainer_info(self.username)
        if not trainer_info:
            return None
        return trainer_info.get("phone")
    
    def get_trainer_email(self):
        trainer_info = self.get_trainer_info(self.username)
        if not trainer_info:
            return None
        return trainer_info.get("email")
    
    def get_trainer_address(self):
        trainer_info = self.get_trainer_info(self.username)
        if not trainer_info:
            return None