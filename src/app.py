"""
Module provide admission to the app
"""

# Modules
import getpass
import controllers.controllers as controller
import views
import constants


def main():
    """
    Function start app and present login
    """
    while constants.MAIN_ENGINE:
        print(constants.SYSTEM_MESSAGE)
        username = input(constants.USER_NAME)
        controller.set_username(username)
        password = input(constants.USER_PASSWORD)
        controller.set_password(password)
        user = controller.validate_user()
        if user is None:
            print(constants.WRONG_USERNAME_PASSWORD)
            print(constants.SEPARATOR)
            continue
        views.load_menu(user)
        constants.MAIN_ENGINE = False

if __name__ == "__main__":
    main()
