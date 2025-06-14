
from basic.login import print_menu
from core.table_queries import initializing_tables
from library.admin import admin_menu, add_book_admin, up_del_admin
from library.users import users_menu, show_books_user, search_by_author, rent_book, return_book, view_rent_book


def main():
    user = print_menu()
    if user[3] == '1':
        while True:
            admin_menu()
            choice = input("Tanlang: ")
            if choice == '1':
                add_book_admin()
            elif choice == '2':
                up_del_admin()
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
                show_books_user()
            elif choice == '2':
                search_by_author()
            elif choice == '3':
                rent_book(user_data=user)
            elif choice == '4':
                return_book(user_data=user)
            elif choice == '5':
                view_rent_book(user_data=user)
            elif choice == '6':
                print("Good bye.")
                return
            else:
                print("Invalid choice.")





if __name__ == '__main__':
    initializing_tables()
    main()