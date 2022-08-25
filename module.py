from flask import redirect


def login(is_logged_in):
    is_logged_in = True
    return is_logged_in


def logout(is_logged_in):
    is_logged_in = False
    return is_logged_in


def check_login(is_logged_in=False):
    if not is_logged_in:
        return redirect('/login', 301)
    return False

