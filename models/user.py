class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def get_role(self):
        return self.role
