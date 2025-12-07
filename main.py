import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QLabel
)
from PySide6.QtCore import Signal, Qt
import sqlite3
from datetime import datetime
from typing import List, Dict

DB_FILE='board.db'

class DBManager:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

# CRUD
    def create_post(self, title: str, content: str, author: str) -> int:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (title, content, author, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, content, author, now, now)
        )
        conn.commit()
        post_id = cur.lastrowid
        conn.close()
        return post_id

    def get_all_posts(self) -> List[Dict]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, created_at, updated_at FROM posts ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [
            {"id": r[0], "title": r[1], "author": r[2], "created_at": r[3], "updated_at": r[4]}
            for r in rows
        ]

    def get_post(self, post_id: int) -> Dict:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, author, created_at, updated_at FROM posts WHERE id = ?", (post_id,))
        r = cur.fetchone()
        conn.close()
        if r:
            return {"id": r[0], "title": r[1], "content": r[2], "author": r[3], "created_at": r[4], "updated_at": r[5]}
        return {}

    def update_post(self, post_id: int, title: str, content: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("UPDATE posts SET title=?, content=?, updated_at=? WHERE id=?", (title, content, now, post_id))
        conn.commit()
        conn.close()

    def delete_post(self, post_id: int):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()
        conn.close()

