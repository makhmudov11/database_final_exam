
from core.database_settings import execute_query


def print_menu():
    print("""
    1.Registratsiya
    2.Login
    """)
    choice = input("Tanlang: ")
    res = False
    if choice == '1':
        while True:
            print("""
            1. Admin
            2. Foydalanuvchi
            """)
            who = input("Tanlang: ")
            if who not in ('1','2'):
                print("Noto'g'ri tanlov.")
                continue
            break
        register(who=who)
        res = login()
        if res is False:
            print_menu()
        return res
    elif choice == '2':
        res = login()
        if res is False:
            print_menu()
        return res
    else:
        print("Invald choice.")
        return print_menu()


def register(who: str):
    print("Registratsiya sahifasi.")

    full_name = input("To'liq ism va familiya kiriting: ")
    email = input("Emailingizni kiriting.")
    query = """
                SELECT * FROM users WHERE full_name = %s AND email = %s AND who = %s;
            """
    params = (full_name, email, who)
    user = execute_query(query=query, params=params, fetch='one')
    if user is not None:
        print("Siz Avval royhatdan otkansiz.")
        return None

    query1 = """

        INSERT INTO users(full_name, email, who) VALUES (%s, %s, %s);
    """

    execute_query(query=query1,params=params)
    print("Siz muvaffaqiyatli royhatdan o'tdingiz")
    return True


def login():
    print("login sahifasi.")

    email = input("Emailingizni kiriting: ").strip()

    query = """
        SELECT * FROM users WHERE email = %s;
    """
    params = (email, )
    user = execute_query(query=query, params=params, fetch='one')

    if user is None:
        print("Siz avval royhatdan o'tishingiz kerak.")
        return False
    return user