import psycopg2

from core.database_settings import execute_query


def admin_menu():
    print("""
     1. Kitob va muallif qo'shish
     2. Kitoblarni tahrirlash va o'chirish
     3. Chiqish
    """)
    return None


def add_book_admin():
    author = input("Muallif ismini kiriting: ")
    book_name = input("Kitob nomini kiriting: ")

    author_query = """
    INSERT INTO authors(full_name) VALUES (%s);
    """
    author_params = (author, )
    execute_query(query=author_query, params=author_params)

    author_id_query  = """SELECT id from authors WHERE full_name = %s;"""
    author_id = execute_query(query=author_id_query, params= (author, ), fetch='one')


    published_at = input("Qachon nashr qilingan: ")
    total_count = input("Umumiy soni: ")
    available_count = total_count
    book_query = """
    INSERT INTO books(nomi, author_id, published_at, total_count, available_count) VALUES(%s, %s, %s, %s, %s);
    """
    book_params = (book_name, author_id[0], published_at, total_count, available_count)

    try:
        execute_query(query=book_query, params=book_params)
        print("Kitob va muallif muvaffaqiyatli qoshildi.")
    except psycopg2.Error as e:
        print(f"Xatolik yuz berdi, {e}")
    finally:
        return None


def up_del_admin():

    print("""
    1. Tahrirlash
    2. Ochirish
    """)
    while True:
        choice = input("tanlang: ")
        if choice in ('1', '2'):
            break
        print("Invalid choice.")

    query = """SELECT * FROM books;"""
    everyone_books = execute_query(query=query, fetch='all')

    print("Mavjud kitoblar: ")
    for book in everyone_books:
        print(f"Nomi: {book[1]}, Muallif id: {book[2]}, Jami miqdori: {book[4]}, Qolgan miqdori: {book[5]}")

    if choice == '1':
        book_name = input("Qaysi kitobni tahrirlash kerak: ")
        search_book = """
        SELECT * FROM books WHERE nomi = %s;
        """
        book_data = execute_query(query=search_book, params=(book_name,), fetch='one')

        if book_data is None:
            print("Siz qidirgan kitob topilmadi")
            return None
        print(f"Nomi: {book_data[1]}, Muallif id: {book_data[2]}, Jami miqdori: {book_data[4]}, Qolgan miqdori: {book_data[5]}")

        print("""
        1. Nomi
        2. Muallif id
        3. Jami miqdori
        4. Qolgan miqdori
        """)
        variant = input("Tanlang: ")

        if variant not in ('1', '2', '3', '4'):
            print("Noto'g'ri tanlov.")
            return None
        if variant == '1':
            nomi = input("Kitob nomini ozgartiring: ")
            update = """UPDATE books SET nomi = %s WHERE id = %s;"""
            params = (nomi, book_data[0])
        elif variant == '2':
            muallif_id = input("Muallif idni ozgartiring: ")
            update = """UPDATE books SET muallif_id = %s WHERE id = %s;"""
            params = (muallif_id, book_data[0])
        elif variant == '3':
            everyone_quantity = input("Jami miqdorini ozgartiring: ")
            update = """UPDATE books SET total_count = %s WHERE id = %s;"""
            params = (everyone_quantity, book_data[0])
        else:
            available_quantity = input("Qolgan miqdorini ozgartiring: ")
            update = """UPDATE books SET available_count = %s WHERE id = %s;"""
            params = (available_quantity, book_data[0])

        try:
            execute_query(query=update, params=params)
            print("Ozgartirish muvaffaqiyatli bajarildi.")
        except psycopg2.Error as e:
            print(f"Tahrirlashda xatolik yuz berdi, {e}")
        finally:
            return None
    else:
        delete_book = input("Qaysi kitobni ochirish kerak: ")

        delete_query = """DELETE FROM books WHERE nomi = %s;"""

        try:
            execute_query(query=delete_query, params=(delete_book, ))
            print("Ochirish muvaffaqiyatli bajarildi.")
        except psycopg2.Error as e:
            print(f"Ochirishda xatolik, {e}")
        finally:
            return None
