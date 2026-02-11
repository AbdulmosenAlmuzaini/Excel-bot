import sqlite3
from datetime import datetime

DB_NAME = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'en',
        msg_count INTEGER DEFAULT 0,
        file_count INTEGER DEFAULT 0,
        last_interaction DATE,
        last_file_upload DATE,
        state TEXT DEFAULT 'NORMAL',
        context TEXT DEFAULT '{}'
    )
    ''')
    
    # Simple migration: add columns if they don't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN state TEXT DEFAULT 'NORMAL'")
        cursor.execute("ALTER TABLE users ADD COLUMN context TEXT DEFAULT '{}'")
    except:
        pass # Already exists
    # Interaction logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        query TEXT,
        response TEXT,
        timestamp DATETIME,
        type TEXT
    )
    ''')
    
    # Feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rating TEXT,
        comment TEXT,
        timestamp DATETIME
    )
    ''')
    
    # Error logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        message TEXT,
        timestamp DATETIME
    )
    ''')
    
    # Full Chat Logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_reply TEXT,
        timestamp DATETIME
    )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(user_id):
    if not get_user(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, last_interaction) VALUES (?, ?)", 
                       (user_id, datetime.now().date()))
        conn.commit()
        conn.close()

def update_user_lang(user_id, lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def log_interaction(user_id, query, response, log_type="text"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, query, response, timestamp, type) VALUES (?, ?, ?, ?, ?)",
                   (user_id, query, response, datetime.now(), log_type))
    conn.commit()
    conn.close()

def check_and_update_limits(user_id, is_file=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now().date()
    
    user = get_user(user_id)
    if not user:
        register_user(user_id)
        user = get_user(user_id)
        
    user_id, lang, msg_count, file_count, last_interaction, last_file_upload, state, context = user
    
    # Reset counts if it's a new day
    if str(last_interaction) != str(today):
        msg_count = 0
        file_count = 0
        last_interaction = today
        
    if is_file:
        file_count += 1
        last_file_upload = today
    else:
        msg_count += 1
        
    cursor.execute('''
        UPDATE users 
        SET msg_count = ?, file_count = ?, last_interaction = ?, last_file_upload = ?
        WHERE user_id = ?
    ''', (msg_count, file_count, last_interaction, last_file_upload, user_id))
    
    conn.commit()
    conn.close()
    return msg_count, file_count

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]
    
    # Error breakdown
    cursor.execute("SELECT category, COUNT(*) FROM error_logs GROUP BY category")
    error_breakdown = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM chat_logs")
    chat_log_count = cursor.fetchone()[0]
    
    conn.close()
    return user_count, total_logs, error_breakdown, chat_log_count

def log_chat(user_id, user_message, bot_reply):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_logs (user_id, user_message, bot_reply, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, user_message, bot_reply, datetime.now()))
    conn.commit()
    conn.close()

def get_admin_logs(limit=20, user_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM chat_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    else:
        cursor.execute("SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = cursor.fetchall()
    conn.close()
    return logs

def export_logs_to_excel():
    import pandas as pd
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM chat_logs", conn)
    conn.close()
    
    file_path = "chat_logs_export.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

def log_error_to_db(user_id, category, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO error_logs (user_id, category, message, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, category, message, datetime.now()))
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Get last N interactions
    cursor.execute('''
        SELECT type, query, response 
        FROM logs 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    formatted_history = []
    # Reverse to get chronological order
    for log_type, query, response in reversed(rows):
        if log_type == "text":
            formatted_history.append({"role": "user", "content": query})
            formatted_history.append({"role": "assistant", "content": response})
    return formatted_history

def clear_chat_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user_state(user_id, state, context_data=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if context_data is not None:
        import json
        cursor.execute("UPDATE users SET state = ?, context = ? WHERE user_id = ?", 
                       (state, json.dumps(context_data), user_id))
    else:
        cursor.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, user_id))
    conn.commit()
    conn.close()

def get_user_state(user_id):
    user = get_user(user_id)
    if user:
        # Indices based on updated schema: user_id(0), lang(1), msg(2), file(3), last_int(4), last_file(5), state(6), context(7)
        # Note: Depending on when user was created, index might be different. 
        # Better query specifically:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT state, context FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            import json
            return row[0], json.loads(row[1])
    return "NORMAL", {}
def log_feedback(user_id, rating, comment=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (user_id, rating, comment, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, rating, comment, datetime.now()))
    conn.commit()
    conn.close()
