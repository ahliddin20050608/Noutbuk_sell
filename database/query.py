import sqlite3

import pdfkit
from database.connect import get_connect 

DB_PATH = "db.sqlite3"

# 🔹 Jadval yaratish
def create_tables():
    conn = get_connect()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        username TEXT,
        phone TEXT,
        is_admin INTEGER DEFAULT 0,
        messages TEXT
    );

    CREATE TABLE IF NOT EXISTS laptops(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        brand TEXT NOT NULL,
        cpu TEXT,
        ram TEXT,
        storage TEXT,
        gpu TEXT,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        image TEXT,
        status TEXT,
        type TEXT
    );

    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        laptop_id INTEGER,
        user_id INTEGER,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        status TEXT DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (laptop_id) REFERENCES laptops(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS admin_messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()


def add_admin_messages_table():
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()



def save_admin_message(admin_id: int, user_id: int, message_text: str):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO admin_messages (admin_id, user_id, message)
        VALUES (?, ?, ?)
    """, (admin_id, user_id, message_text))
    conn.commit()
    conn.close()


def get_admin_messages():
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, admin_id, user_id, message, timestamp
        FROM admin_messages
        ORDER BY timestamp DESC
    """)
    messages = cursor.fetchall()
    conn.close()
    return messages





def get_users():
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, chat_id, name, username, phone, messages FROM users")
    users = cursor.fetchall()
    conn.close()
    return users




# 🔹 messages ustunini qo‘shish
def add_messages_column():
    conn = get_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN messages TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Agar ustun allaqachon mavjud bo‘lsa, xatolikni e'tiborsiz qoldiramiz
        pass
    finally:
        conn.close()
def save_user_message(chat_id: int, message_text: str):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM users WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    existing_messages = result[0] if result and result[0] else ""
    updated_messages = existing_messages + ("\n" if existing_messages else "") + message_text
    cursor.execute("UPDATE users SET messages = ? WHERE chat_id = ?", (updated_messages, chat_id))
    conn.commit()
    conn.close()


# 🔹 Foydalanuvchini tekshirish
def is_registered_by_chat_id(chat_id: int) -> bool:
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# 🔹 Adminligini tekshirish
def is_admin(chat_id: int) -> bool:
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE chat_id = ?", (chat_id,))
    user = cursor.fetchone()
    conn.close()
    return bool(user and user[0] == 1)


# 🔹 Foydalanuvchi xabarlarini olish
def get_user_all_messages(chat_id: int) -> str | None:
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM users WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None


def get_laptops(category=None, status=None):
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row  # 🔹 har bir qator dict ko‘rinishida chiqadi
    cursor = conn.cursor()

    if category and status:
        cursor.execute("SELECT * FROM laptops WHERE type = ? AND status = ?", (category, status))
    elif category:
        cursor.execute("SELECT * FROM laptops WHERE type = ?", (category,))
    else:
        cursor.execute("SELECT * FROM laptops")

    laptops = cursor.fetchall()
    conn.close()
    return laptops



def insert_laptop(
    title: str,
    description: str = None,
    brand: str = None,
    cpu: str = None,
    ram: str = None,
    storage: str = None,
    gpu: str = None,
    price: int = 0,
    quantity: int = 1,
    image: str = None,
    status: str = "new",
    type_: str = "programming"
):
    conn = get_connect()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO laptops
        (title, description, brand, cpu, ram, storage, gpu, price, quantity, image, status, type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title, description, brand, cpu, ram, storage, gpu, price, quantity, image, status, type_
    ))
    
    conn.commit()
    conn.close()
    print(f"✅ Laptop '{title}' bazaga qo‘shildi.")

# 🔹 Adminlar
def get_admins():
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users WHERE is_admin = 1")
    admins = [row[0] for row in cursor.fetchall()]
    conn.close()
    return admins

# 🔹 Telefon raqamini olish
def get_user_phone(chat_id: int) -> str | None:
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM users WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None

# 🔹 Laptoplarni PDF ga chiqarish
def generate_laptops_pdf(laptops, category, status, file_path="laptops.pdf"):
    html_content = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        <h2>{category.capitalize()} noutbuklari ({status.capitalize()})</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Brand</th>
                <th>CPU</th>
                <th>RAM</th>
                <th>Storage</th>
                <th>GPU</th>
                <th>Price</th>
            </tr>
    """

    for lap in laptops:
        html_content += f"""
            <tr>
                <td>{lap['title']}</td>
                <td>{lap['brand']}</td>
                <td>{lap['cpu']}</td>
                <td>{lap['ram']}</td>
                <td>{lap['storage']}</td>
                <td>{lap['gpu']}</td>
                <td>{lap['price']} 💰</td>
            </tr>
        """

    html_content += "</table></body></html>"

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdfkit.from_string(html_content, file_path, configuration=config)
    return file_path

def get_user_messages():
    """
    Bazadagi barcha foydalanuvchilarning messages ustunini oladi.
    """
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, username, messages FROM users WHERE messages IS NOT NULL AND messages != ''")
    messages = cursor.fetchall()
    conn.close()
    return messages




def save_user(chat_id: int, name: str, username: str = None, phone: str = None):
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (chat_id, name, username, phone)
        VALUES (?, ?, ?, ?)
    """, (chat_id, name, username, phone))

    conn.commit()
    conn.close()



