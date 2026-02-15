import sqlite3
DB_NAME = "bot_database.db"

def check_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, language FROM users")
    rows = cursor.fetchall()
    print("Users in DB:")
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    check_db()
