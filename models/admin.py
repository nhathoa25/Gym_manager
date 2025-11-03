from models.user import User
from data_work.info_add import add_user_to_json
from data_work.info_add import add_trainer_to_json
from data_work.info_add import change_equipment_in_json
from data_work.info_add import change_subscription_in_json
from data_work.info_add import delete_user_from_json
from data_work.info_add import search_members_by_name
from data_work.info_add import update_member_info
from data_work.info_add import calculate_revenue_data
from data_work.info_add import search_trainer_by_name
from data_work.info_add import add_attendance_day_to_json

import json
import os

class Admin(User):
    def __init__(self, username):
        super().__init__(username, "admin")
        self._permissions = [
            "manage_members", "manage_trainers", "manage_equipment",
            "view_reports", "manage_system", "delete_users"
        ]

    def get_display_name(self):
        """Get display name for admin"""
        return f"Admin: {self.username}"

    def can_perform_action(self, action):
        """Check if admin can perform a specific action"""
        return action in self._permissions

    def get_permissions(self):
        """Get list of admin permissions"""
        return self._permissions.copy()

    def new_member(self, member_data):
        try:
            add_user_to_json(**member_data)
            return True
        except Exception as e:
            print(f"Error adding member: {e}")
            return False

    def new_trainer(self, trainer_data):
        try:
            add_trainer_to_json(**trainer_data)
            return True
        except Exception as e:
            print(f"Error adding trainer: {e}")
            return False

    def save_equipment_data(self, equipment_data):
        try:
            change_equipment_in_json(equipment_data)
            return True
        except Exception as e:
            print(f"Error saving equipment data: {e}")
            return False

    def delete_member(self, username):
        try:
            delete_user_from_json(username)
            return True
        except Exception as e:
            print(f"Error deleting member: {e}")
            return False

    def search_members(self, search_term):
        try:
            return search_members_by_name(search_term)
        except Exception as e:
            print(f"Error searching members: {e}")
            return []
    def search_trainer(self, search_term):
        try:
            return search_trainer_by_name(search_term)
        except Exception as e:
            print(f"Error searching trainers: {e}")
            return []
    def update_member(self, username, updated_data):
        try:
            return update_member_info(username, updated_data)
        except Exception as e:
            print(f"Error updating member: {e}")
            return False

    def save_subscription_data(self, subscription_data):
        try:
            change_subscription_in_json(subscription_data)
            return True
        except Exception as e:
            print(f"Error saving subscription data: {e}")
            return False

    def calculate_revenue(self):
        """Calculate revenue data using the function from info_add"""
        try:
            return calculate_revenue_data()
        except Exception as e:
            print(f"Error calculating revenue: {e}")
            return {
                'total_revenue': 0,
                'revenue_by_plan': {},
                'revenue_by_month': {},
                'member_details': [],
                'total_members': 0
            }
    def attendance_report(self):
        try:
            return attendance_report_data()
        except Exception as e:
            print(f"Error generating attendance report: {e}")
            return []
    def add_attendance_day(self, username, date):
        try:
            return add_attendance_day_to_json(username, date)
        except Exception as e:
            print(f"Error adding attendance day: {e}")
            return False
    def add_workout_day(self, username, date, workout):
        try:
            return add_workout_day_to_json(username, date, workout)
        except Exception as e:
            print(f"Error adding workout day: {e}")
            return False