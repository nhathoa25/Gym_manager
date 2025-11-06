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
        """
        Renew or subscribe the current member to a new plan.

        Behavior:
        - Expects self.username to be set.
        - Reads `data/subscription_info.json` to get plan duration and price.
        - Reads `data/member_info.json`, finds the member record and updates
          `membership` and `subscription_expiry`.
        - If the existing expiry is in the future, the new duration is added to it;
          otherwise it starts from today.
        - Returns a dict with result information: {'success': bool, 'message': str, 'new_expiry': str, 'price': int}
        """
        try:
            with open("data/subscription_info.json", "r", encoding="utf-8") as f:
                plans = json.load(f)
        except Exception as e:
            return {"success": False, "message": f"Could not read subscription info: {e}"}

        # This method is intended to be called with a chosen plan name provided by a GUI.
        # To keep compatibility, if it's called without a parameter we do nothing.
        return {"success": False, "message": "No plan specified. Use Member.renew_subscribe_plan_with_name(plan_name)"}

    def renew_subscribe_plan_with_name(self, plan_name):
        """Renew/subscribe to a specific plan name (string)."""
        if not plan_name:
            return {"success": False, "message": "No plan name provided."}

        try:
            with open("data/subscription_info.json", "r", encoding="utf-8") as f:
                plans = json.load(f)
        except Exception as e:
            return {"success": False, "message": f"Could not read subscription info: {e}"}

        plan_detail = plans.get(plan_name)
        if not plan_detail or not isinstance(plan_detail, list) or len(plan_detail) < 1:
            return {"success": False, "message": f"Plan '{plan_name}' not found."}

        try:
            duration_days = int(plan_detail[0])
        except Exception:
            duration_days = 0

        price = None
        if isinstance(plan_detail, list) and len(plan_detail) >= 2:
            try:
                price = int(plan_detail[1])
            except Exception:
                price = None

        # Load members
        try:
            with open("data/member_info.json", "r", encoding="utf-8") as f:
                members = json.load(f)
        except Exception as e:
            return {"success": False, "message": f"Could not read member info: {e}"}

        found = False
        for m in members:
            if m.get("username") == self.username:
                found = True
                # parse existing expiry
                today = datetime.now().date()
                current_expiry_str = m.get("subscription_expiry")
                base_date = today
                if current_expiry_str:
                    try:
                        parts = current_expiry_str.split("-")
                        y, mo, d = map(int, parts)
                        current_expiry = datetime(y, mo, d).date()
                        if current_expiry > today:
                            base_date = current_expiry
                    except Exception:
                        base_date = today

                new_expiry_date = base_date + timedelta(days=duration_days)
                # Format as YYYY-MM-DD
                new_expiry_str = new_expiry_date.strftime("%Y-%m-%d")

                m["membership"] = plan_name
                m["subscription_expiry"] = new_expiry_str
                break

        if not found:
            return {"success": False, "message": f"Member '{self.username}' not found."}

        # Save members back
        try:
            with open("data/member_info.json", "w", encoding="utf-8") as f:
                json.dump(members, f, indent=4, ensure_ascii=False)
        except Exception as e:
            return {"success": False, "message": f"Failed to write member info: {e}"}

        return {"success": True, "message": "Subscription updated.", "new_expiry": new_expiry_str, "price": price, "plan": plan_name}

    def check_workout_schedule(self):
        pass
    
    def view_subscription(self):
        pass