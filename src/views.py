"""
View module provide user interface
"""

import controllers.controllers as controller
import constants as constant


def load_menu(user):
    """
    Function load menu for each user role,
    depends of session role
    """
    controller.set_first_name(user["name"])
    controller.set_last_name(user["lastname"])
    if user["role"] == "manager":
        load_manager_menu()
    elif user["role"] == "seller":
        load_seller_menu()
    else:
        print('Trenutno nije kreiran meni za tu vrstu role.')
        return


def load_manager_menu():
    """
    Function provide manager menu view,
    and controller over menu options
    """
    while constant.MANAGER_MAIN_ENGINE:
        controller.print_session_message()
        try:
            print(constant.CHOSE_MENU_OPTION)
            option = int(controller.print_manager_menu_options())
            if option == 1:
                load_search_event_menu()
            elif option == 2:
                controller.add_event()
            elif option == 3:
                events = controller.get_events()
                controller.print_table(events)
                event_id = int(input("Unesite ID projekcije - "))
                controller.delete_event_by_id(event_id)
            elif option == 4:
                controller.update_event()
            elif option == 5:
                controller.add_new_user()
            elif option == 6:
                print(constant.GOODBYE_MESSAGE)
                break
            else:
                print(constant.WRONG_INPUT_OPTION)
        except ValueError:
            print(constant.VALUE_ERROR_MESSAGE)


def load_seller_menu():
    """
    Function provide manager menu view,
    and controller over menu options
    """
    while constant.SELLER_MAIN_ENGINE:
        controller.print_session_message()
        try:
            print(constant.CHOSE_MENU_OPTION)
            menu_option = int(controller.print_seller_menu_options())
            if menu_option == 1:
                load_search_event_menu()
            elif menu_option == 2:
                controller.sell_ticet()
            elif menu_option == 3:
                controller.print_table_tickets()
            elif menu_option == 4:
                print(constant.GOODBYE_MESSAGE)
                break
            else:
                print(constant.WRONG_INPUT_OPTION)
        except ValueError:
            print(constant.VALUE_ERROR_MESSAGE)


def load_search_event_menu():
    """
    Function provide search event view,
    and controller function that help
    control over search options
    """
    while constant.SEARCH_EVENTS_ENGINE:
        try:
            print(constant.CHOSE_SEARCH_EVENT_OPTION)
            event_option = int(controller.print_search_events_menu_options())
            if event_option == 1:
                controller.all_events()
            elif event_option == 2:
                event_id = int(input("Unesite ID filma - "))
                controller.find_by_id(event_id)
            elif event_option == 3:
                event_movie_name = input("Unesite ime filma - ")
                controller.find_by_movie_name(event_movie_name)
            elif event_option == 4:
                event_movie_type = input('Unesite tip filma - ')
                controller.find_event_by_movie_type(event_movie_type.lower())
            elif event_option == 5:
                hall_id = input("Unesite ID sale - ")
                controller.find_by_hall(hall_id)
            elif event_option == 6:
                print(constant.GOODBYE_MESSAGE)
                break
            else:
                print(constant.WRONG_INPUT_OPTION)
        except ValueError:
            print(constant.VALUE_ERROR_MESSAGE)
