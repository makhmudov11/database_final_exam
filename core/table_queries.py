from core.database_settings import execute_query

table1 = """
CREATE TABLE IF NOT EXISTS authors (
id SERIAL PRIMARY KEY,
full_name VARCHAR(50)
);
"""
table2 = """
CREATE TABLE IF NOT EXISTS books (
id SERIAL PRIMARY KEY,
nomi TEXT NOT NULL,
author_id INTEGER REFERENCES authors(id),
published_at DATE,
total_count INTEGER,
available_count INTEGER
);
"""
table3 = """
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
full_name VARCHAR(50) NOT NULL,
email VARCHAR(30) UNIQUE NOT NULL
);
"""
table4 = """
CREATE TABLE IF NOT EXISTS check_books (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES users(id),
book_id INTEGER REFERENCES books(id),
borrowed_at DATE,
returned_at DATE
);
"""
def initializing_tables():
    execute_query(query=table1)
    execute_query(query=table2)
    execute_query(query=table3)
    execute_query(query=table4)
    return None
