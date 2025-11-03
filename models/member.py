from models.user import User
from datetime import datetime, timedelta
import json
from guis.member_guis.contact import show_contact_window

class Member(User):
    def __init__(self, username):
        super().__init__(username, "member")
        self.membership_expiry = None
        self.attendance_records = []
        self.personal_trainer = None

    def get_member_info(username):
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            members = json.load(f)
        for m in members:
            if m["username"] == username:
                return m
        return None

    def get_trainer_phone(self):
        member_info = self.get_member_info(self.username)
        if not member_info:
            return None
        trainer_username = member_info.get("trainer_username")
        if not trainer_username:
            return None
        # Import here to avoid circular import
        from guis.member_guis.contact import get_trainer_phone
        return get_trainer_phone(trainer_username)

    def get_trainer_email(self):
        member_info = self.get_member_info(self.username)
        if not member_info:
            return None
        trainer_username = member_info.get("trainer_username")
        if not trainer_username:
            return None
    

    def show_contact_info(self):
        pass

    def contact_trainers_admin(self):
        pass

    def renew_subscribe_plan(self):
        pass

    def check_workout_schedule(self):
        pass
    
    def view_subscription(self):
        pass