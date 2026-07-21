import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("storage").mkdir(
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            "storage/database.db"
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filepath TEXT,

            action TEXT,

            created_at TEXT

        )
        """)

        self.connection.commit()

    def insert(self, filepath, action, created_at):

        self.cursor.execute("""

        INSERT INTO history

        (filepath,action,created_at)

        VALUES(?,?,?)

        """,

        (filepath, action, created_at)

        )

        self.connection.commit()

    def all(self):

        self.cursor.execute(

            "SELECT * FROM history"

        )

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()