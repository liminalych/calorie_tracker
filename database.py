import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("calorie_tracker.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица профилей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        # Таблица продуктов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                calories REAL,
                protein REAL,
                fat REAL,
                carbs REAL
            )
        ''')
        # Таблица дневного приёма пищи
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                product_id INTEGER,
                quantity REAL,
                profile_id INTEGER,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            )
        ''')
        self.conn.commit()

    # ==== Профили ====
    def get_profiles(self):
        self.cursor.execute("SELECT id, name FROM profiles")
        return self.cursor.fetchall()

    def add_profile(self, name):
        try:
            self.cursor.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    # ==== Продукты ====
    def add_product(self, name, calories, protein, fat, carbs):
        try:
            self.cursor.execute(
                "INSERT INTO products (name, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?)",
                (name, calories, protein, fat, carbs)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_products(self):
        self.cursor.execute("SELECT id, name FROM products")
        return self.cursor.fetchall()

    def get_product(self, product_id):
        self.cursor.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        )
        return self.cursor.fetchone()

    def update_product(self, product_id, name, calories, protein, fat, carbs):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE products
                SET name = ?, calories = ?, protein = ?, fat = ?, carbs = ?
                WHERE id = ?
            """, (name, calories, protein, fat, carbs, product_id))
            self.conn.commit()
            return True
        except:
            return False

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM daily_intake WHERE product_id=?", (product_id,))
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    # ==== Дневной приём пищи ====
    def add_daily_entry(self, date, product_id, quantity, profile_id):
        self.cursor.execute(
            "INSERT INTO daily_intake (date, product_id, quantity, profile_id) VALUES (?, ?, ?, ?)",
            (date, product_id, quantity, profile_id)
        )
        self.conn.commit()

    def get_daily_entries_with_id(self, date, profile_id):
        self.cursor.execute(
            '''
            SELECT di.id, p.name, di.quantity, p.calories, p.protein, p.fat, p.carbs
            FROM daily_intake di
            JOIN products p ON di.product_id = p.id
            WHERE di.date = ? AND di.profile_id = ?
            ''',
            (date, profile_id)
        )
        return self.cursor.fetchall()

    def get_daily_entry(self, entry_id):
        self.cursor.execute(
            "SELECT * FROM daily_intake WHERE id = ?", (entry_id,)
        )
        return self.cursor.fetchone()

    def update_daily_entry(self, entry_id, date, quantity):
        self.cursor.execute(
            "UPDATE daily_intake SET date=?, quantity=? WHERE id=?",
            (date, quantity, entry_id)
        )
        self.conn.commit()

    def delete_daily_entry(self, entry_id):
        self.cursor.execute("DELETE FROM daily_intake WHERE id=?", (entry_id,))
        self.conn.commit()
