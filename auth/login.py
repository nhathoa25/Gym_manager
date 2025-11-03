from data_work.auth_add import check_credentials

def authenticate_user(username, password):
    """
    Authenticate a user with the given username and password.
    
    Args:
        username (str): The username to authenticate
        password (str): The password to authenticate
        
    Returns:
        tuple: (username, role) if authentication successful, None otherwise
    """
    if not username or not password:
        return None
    
    role = check_credentials(username, password)
    
    if role is not None:
        return username, role
    else:
        return None

def validate_login_input(username, password):
    """
    Validate login input fields.
    
    Args:
        username (str): The username to validate
        password (str): The password to validate
        
    Returns:
        tuple: (is_valid, error_message) where is_valid is boolean and error_message is str
    """
    if not username.strip():
        return False, "Username cannot be empty"
    
    if not password.strip():
        return False, "Password cannot be empty"
    
    return True, "" 