import sqlite3

def create_connection():
    conn = sqlite3.connect('budget.db')
    return conn

def setup_database():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL, type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recurring_transactions
                 (id INTEGER PRIMARY KEY, start_date TEXT, description TEXT, amount REAL, type TEXT, frequency TEXT)''')
    conn.commit()
    conn.close()
