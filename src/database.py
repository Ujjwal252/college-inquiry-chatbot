from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import pandas as pd

from utils.config import DB_PATH


class ChatDatabase:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                intent TEXT,
                confidence REAL,
                timestamp TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                rating INTEGER NOT NULL,
                comment TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(chat_id) REFERENCES chat_logs(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS faq_searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT NOT NULL,
                matched_intent TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )

        self.conn.commit()

    def log_conversation(
        self,
        user_msg: str,
        bot_response: str,
        intent: str,
        confidence: float,
    ) -> int:
        cursor = self.conn.cursor()
        ts = datetime.now().isoformat(timespec="seconds")
        cursor.execute(
            """
            INSERT INTO chat_logs (user_message, bot_response, intent, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_msg, bot_response, intent, confidence, ts),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def add_feedback(self, chat_id: int, rating: int, comment: str | None) -> int:
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        cursor = self.conn.cursor()
        ts = datetime.now().isoformat(timespec="seconds")
        cursor.execute(
            """
            INSERT INTO feedback (chat_id, rating, comment, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, int(rating), comment, ts),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def get_recent_chats(self, limit: int = 50) -> pd.DataFrame:
        query = """
            SELECT id, user_message, bot_response, intent, confidence, timestamp
            FROM chat_logs
            ORDER BY id DESC
            LIMIT ?
        """
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def get_intent_analytics(self) -> pd.DataFrame:
        query = """
            SELECT intent, COUNT(*) as count
            FROM chat_logs
            GROUP BY intent
            ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_top_queries(self, limit: int = 10) -> pd.DataFrame:
        query = """
            SELECT user_message, COUNT(*) as count
            FROM chat_logs
            GROUP BY user_message
            ORDER BY count DESC
            LIMIT ?
        """
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def export_to_csv(self, filepath: str) -> None:
        df = pd.read_sql_query(
            """
            SELECT id, user_message, bot_response, intent, confidence, timestamp
            FROM chat_logs
            ORDER BY id DESC
            """,
            self.conn,
        )
        df.to_csv(filepath, index=False)

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

