from .terminal_menu import show_main_menu, choose_main_menu


def run_terminal():
    while True:
        try:
            show_main_menu()
            choose_main_menu()
        except Exception as e:
            print(e)

