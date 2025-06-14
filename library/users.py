import psycopg2

from core.database_settings import execute_query
from datetime import datetime

def users_menu():
    print("""
    1. Kitoblar ro'yxatini ko'rish
    2. Muallif bo'yicha kitoblarni qidirish
    3. Kitobni ijaraga olish
    4. Kitobni qaytarish
    5. O'z ijaralarini ko'rish
    6. Chiqish
    """)
    return None


def show_books_user():
    query = """SELECT * FROM books ORDER BY id;"""
    everyone_books = execute_query(query=query, fetch='all')

    print("Mavjud kitoblar: ")
    for book in everyone_books:
        print(f"Nomi: {book[1]}, Qolgan miqdori: {book[5]}")
    return


def search_by_author():
    author_name = input("Muallif nomini kiriting: ")

    id_query = "SELECT id FROM authors WHERE full_name = %s;"
    author_id = execute_query(query=id_query, params=(author_name,), fetch='one')

    if author_id is None:
        return "Ma'lumot topilmadi."

    books_query = """
    SELECT b.nomi, a.full_name 
    FROM books AS b
    JOIN authors AS a ON b.author_id = a.id
    WHERE a.id = %s;
    """

    res = execute_query(query=books_query, params=(author_id[0], ), fetch='all')

    if not res:
        print("Bu muallifga tegishli kitoblar topilmadi.")
    else:
        for book in res:
            print(f"Kitob nomi: {book[0]}, Muallif: {book[1]}")

    return None

def rent_book(user_data: list):
    query = """SELECT * FROM books ORDER BY id;"""
    everyone_books = execute_query(query=query, fetch='all')

    print("Mavjud kitoblar: ")
    for book in everyone_books:
        print(f"Nomi: {book[1]}, Qolgan miqdori: {book[5]}")

    book_name = input("Qaysi kitobni ijaraga olasiz: ")
    user_book = None
    for book in everyone_books:
        if book_name.lower() == book[1].lower():
            user_book = book
            break

    if user_book is None:
        print("siz bergan kitob topilmadi.")
        return None

    if user_book[5] > 0:
        book_query = """UPDATE books SET available_total = available_total - 1 WHERE id = %s;"""
        try:
            execute_query(query=book_query, params=(user_book[0], ))
        except psycopg2.Error as e:
            print(f"Kitob ijarasida muammo, {e}")

        add_rent_book = """INSERT INTO check_books(user_id, book_id, borrowed_at) VALUES(%s, %s, %s);"""
        hozir = datetime.now()
        sana = hozir.date()
        values = (user_data[0], user_book[0], sana)

        try:
            execute_query(query=add_rent_book, params=values)
            print("Kitob ijarasi muvaffaqiyatli bajarildi.")
        except psycopg2.Error as e:
            print(f"ijaraga olishda xatolik, {e}")
        finally:
            return None


def return_book(user_data: list):

    print_book_query = """SELECT b.nomi
    FROM books AS b
    INNER JOIN check_books AS c ON b.id = c.book_id
    WHERE c.returned_at IS NULL and user_id = %s;"""

    res = execute_query(query=print_book_query,params=(user_data[0],), fetch='all')


    print("Siz ijaraga olib qaytarmgan kitoblar: ")
    for index, book in enumerate(res, start=1):
        print(f"{index}. {book[0]}")
        index += 1

    book_name = input("Qaytarmoqchi bolgan kitob nomini kiriting: ")


    book_id_query = """SELECT * FROM books WHERE nomi = %s;"""
    book_id = execute_query(query=book_id_query, params=(book_name, ), fetch='one')

    book_query = """
    UPDATE check_books 
    SET returned_at = %s 
    WHERE book_id = %s AND returned_at IS NULL AND user_id = %s;
    """
    hozir = datetime.now()
    sana = hozir.date()

    try:
        execute_query(query=book_query, params=(sana, book_id[0],user_data[0]))
        print("Kitobni ijarasi qaytarildi.")
    except psycopg2.Error as e:
        print(f"Xatolik, {e}")
    finally:
        return None

def view_rent_book(user_data):
    print("Ijaraga olingan kitoblar:")

    query = """
    SELECT b.nomi
    FROM books AS b
    INNER JOIN check_books AS c ON c.book_id = b.id
    WHERE c.user_id = %s AND c.returned_at IS NULL;
    """

    result = execute_query(query=query, params=(user_data[0], ), fetch='all')

    if not result:
        print("Sizda ijaraga olingan kitoblar yo‘q.")
    else:
        for index, book in enumerate(result, start=1):
            print(f"{index}. {book[0]}")
