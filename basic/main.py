
from basic.login import print_menu
from core.table_queries import initializing_tables
from library.admin import admin_menu
from library.users import users_menu


def main():
    user = print_menu()
    if user[3] == '1':
        while True:
            admin_menu()
            choice = input("Tanlang: ")
            if choice == '1':
                pass# add_book_admin()
            elif choice == '2':
                pass
            elif choice == '3':
                print("Good bye!")
                return
            else:
                print("invalid choice.")
    else:
        while True:
            users_menu()
            choice = input("Tanlang: ")
            if choice == '1':
                pass
            elif choice == '2':
                pass
            elif choice == '3':
                pass
            elif choice == '4':
                pass
            elif choice == '5':
                pass
            elif choice == '6':
                print("Good bye.")
                return
            else:
                print("Invalid choice.")





if __name__ == '__main__':
    initializing_tables()
    main()