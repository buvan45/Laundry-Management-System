import sqlite3

def connect():
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT,
            cloth_type TEXT,
            laundry_type TEXT,
            cost REAL,
            delivery_date TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def insert_user(username, email, password):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

def check_email_unique(email):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user is None

def insert_order(user_id,username, cloth_type, laundry_type, cost, delivery_date, status):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (user_id,username, cloth_type, laundry_type, cost, delivery_date, status) VALUES (?, ?, ?, ?, ?, ?,?)", (user_id, username,cloth_type, laundry_type, cost, delivery_date, status))
    conn.commit()
    conn.close()

def get_orders_by_user(user_id):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
    orders = cur.fetchall()
    conn.close()
    return orders

def update_user_info(user_id, name, phone, email):
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("laundry.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return users

def get_report():
    try:
        conn = sqlite3.connect("laundry.db")
        cur = conn.cursor()
        # Modified query to retrieve user and cloth information

        # id INTEGER PRIMARY KEY,
        #     user_id INTEGER,
        #     cloth_type TEXT,
        #     laundry_type TEXT,
        #     cost REAL,
        #     delivery_date TEXT,
        #     status TEXT,
        #     FOREIGN KEY(user_id) REFERENCES users(id)

        query = """
            SELECT users.username, users.email, orders.cloth_type, orders.laundry_type, orders.cost, orders.delivery_date, orders.status
            FROM orders
            INNER JOIN users
            ON orders.username = users.username
        """
        
        print("Executing query:", query)  # Debug print
        cur.execute(query)
        report = cur.fetchall()
        print("Report:", report)  # Debug print
        conn.close()
        return report
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None
    
def update_status(username, cloth_type, laundry_type, cost, new_status):
    try:
        conn = sqlite3.connect("laundry.db")
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders
            SET status = ?
            WHERE username = ? AND cloth_type = ? AND laundry_type = ? AND cost = ?
        """, (new_status, username, cloth_type, laundry_type, cost))
        print("Updated status to", new_status)  # Debug print   
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

