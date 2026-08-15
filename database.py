import sqlite3
import asyncio
from typing import Dict, Any, List

DB_PATH = "bot_data.db"


class Database:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS metrics (
                    key TEXT PRIMARY KEY,
                    value INTEGER DEFAULT 0
                )
            """
            )
            metrics = ["images_processed", "successful_ops", "failed_ops"]
            for metric in metrics:
                cursor.execute(
                    "INSERT OR IGNORE INTO metrics (key, value) VALUES (?, 0)",
                    (metric,),
                )
            conn.commit()

    async def add_user(self, user_id: int, username: str):
        def _execute():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                    (user_id, username),
                )
                conn.commit()

        await asyncio.to_thread(_execute)

    async def increment_metric(self, key: str):
        def _execute():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE metrics SET value = value + 1 WHERE key = ?",
                    (key,),
                )
                conn.commit()

        await asyncio.to_thread(_execute)

    async def get_stats(self) -> Dict[str, Any]:
        def _execute():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]

                cursor.execute("SELECT key, value FROM metrics")
                metrics = dict(cursor.fetchall())

                return {
                    "total_users": total_users,
                    "images_processed": metrics.get("images_processed", 0),
                    "successful_ops": metrics.get("successful_ops", 0),
                    "failed_ops": metrics.get("failed_ops", 0),
                }

        return await asyncio.to_thread(_execute)

    async def get_all_user_ids(self) -> List[int]:
        def _execute():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users")
                return [row[0] for row in cursor.fetchall()]

        return await asyncio.to_thread(_execute)


db = Database()
