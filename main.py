from guis.login_window import open_login_window
from models.admin import Admin
from models.trainer import Trainer
from models.member import Member

from guis.admin_window import open_admin_window
from guis.trainer_window import open_trainer_window
from guis.member_window import open_member_window

def main():

    username, role = open_login_window()

    if role == "admin":
        admin_user = Admin(username)
        open_admin_window(admin_user)

    elif role == "trainer":
        trainer_user = Trainer(username)
        open_trainer_window(trainer_user)

    elif role == "member":
        member_user = Member(username)
        open_member_window(member_user)
        print(f"Member functionality not yet implemented for {username}")

    else:
        print("Login failed.")

if __name__ == "__main__":
    main()