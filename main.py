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

DB_FILE = 'board.db'


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
        cur.execute(
            "SELECT id, title, author, created_at, updated_at FROM posts ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [
            {"id": r[0], "title": r[1], "author": r[2],
                "created_at": r[3], "updated_at": r[4]}
            for r in rows
        ]

    def get_post(self, post_id: int) -> Dict:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, content, author, created_at, updated_at FROM posts WHERE id = ?", (post_id,))
        r = cur.fetchone()
        conn.close()
        if r:
            return {"id": r[0], "title": r[1], "content": r[2], "author": r[3], "created_at": r[4], "updated_at": r[5]}
        return {}

    def update_post(self, post_id: int, title: str, content: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("UPDATE posts SET title=?, content=?, updated_at=? WHERE id=?",
                    (title, content, now, post_id))
        conn.commit()
        conn.close()

    def delete_post(self, post_id: int):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()
        conn.close()


class PostListPage(QWidget):
    post_selected = Signal(int)
    create_clicked = Signal()

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        layout = QVBoxLayout()

        title = QLabel("📋 게시판 목록")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작성자", "작성일"])
        self.table.cellClicked.connect(self._on_cell_clicked)
        layout.addWidget(self.table)

        btn_create = QPushButton("새 글 작성")
        btn_create.clicked.connect(self.create_clicked.emit)
        layout.addWidget(btn_create)

        self.setLayout(layout)
        self.load_posts()

    def load_posts(self):
        posts = self.db.get_all_posts()
        self.table.setRowCount(len(posts))
        for i, p in enumerate(posts):
            self.table.setItem(i, 0, QTableWidgetItem(str(p["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(p["title"]))
            self.table.setItem(i, 2, QTableWidgetItem(p["author"]))
            self.table.setItem(i, 3, QTableWidgetItem(p["created_at"]))

    def _on_cell_clicked(self, row, col):
        post_id = int(self.table.item(row, 0).text())
        self.post_selected.emit(post_id)


class PostDetailPage(QWidget):
    back_clicked = Signal()
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self.post_id = None

        layout = QVBoxLayout()

        self.title = QLabel()
        layout.addWidget(self.title)

        self.content = QLabel()
        self.content.setWordWrap(True)
        layout.addWidget(self.content)

        self.info = QLabel()
        layout.addWidget(self.info)

        btns = QHBoxLayout()
        btn_back = QPushButton("뒤로")
        btn_back.clicked.connect(self.back_clicked.emit)
        btns.addWidget(btn_back)

        btn_edit = QPushButton("수정")
        btn_edit.clicked.connect(self._edit)
        btns.addWidget(btn_edit)

        btn_delete = QPushButton("삭제")
        btn_delete.clicked.connect(self._delete)
        btns.addWidget(btn_delete)

        layout.addLayout(btns)
        self.setLayout(layout)

    def load_post(self, post_id):
        self.post_id = post_id
        post = self.db.get_post(post_id)
        self.title.setText(f"제목: {post['title']}")
        self.content.setText(post["content"])
        self.info.setText(
            f"작성자 {post['author']} | 작성일 {post['created_at']} | 수정일 {post['updated_at']}")

    def _edit(self):
        self.edit_clicked.emit(self.post_id)

    def _delete(self):
        self.delete_clicked.emit(self.post_id)


class PostEditPage(QWidget):
    submitted = Signal(int, str, str)
    cancelled = Signal()

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self.post_id = None

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("제목"))
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_input)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("취소")
        btn_cancel.clicked.connect(self.cancelled.emit)
        btns.addWidget(btn_cancel)

        btn_submit = QPushButton("저장")
        btn_submit.clicked.connect(self._submit)
        btns.addWidget(btn_submit)

        layout.addLayout(btns)
        self.setLayout(layout)

    def load_post(self, post_id):
        self.post_id = post_id
        post = self.db.get_post(post_id)
        self.title_input.setText(post["title"])
        self.content_input.setText(post["content"])

    def _submit(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        self.submitted.emit(self.post_id, title, content)


class NewPostPage(QWidget):
    submitted = Signal(str, str, str)
    cancelled = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("제목"))
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_input)

        self.author_input = QLineEdit()
        layout.addWidget(QLabel("작성자"))
        layout.addWidget(self.author_input)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("취소")
        btn_cancel.clicked.connect(self.cancelled.emit)
        btns.addWidget(btn_cancel)

        btn_submit = QPushButton("등록")
        btn_submit.clicked.connect(self._submit)
        btns.addWidget(btn_submit)

        layout.addLayout(btns)
        self.setLayout(layout)

    def _submit(self):
        self.submitted.emit(
            self.title_input.text(),
            self.content_input.toPlainText(),
            self.author_input.text()
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DBManager()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_list = PostListPage(self.db)
        self.page_detail = PostDetailPage(self.db)
        self.page_edit = PostEditPage(self.db)
        self.page_new = NewPostPage()

        self.stack.addWidget(self.page_list)
        self.stack.addWidget(self.page_detail)
        self.stack.addWidget(self.page_edit)
        self.stack.addWidget(self.page_new)

        # 시그널 연결
        self.page_list.post_selected.connect(self.show_detail)
        self.page_list.create_clicked.connect(self.show_new_post)

        self.page_detail.back_clicked.connect(self.show_list)
        self.page_detail.edit_clicked.connect(self.show_edit)
        self.page_detail.delete_clicked.connect(self.delete_post)

        self.page_edit.submitted.connect(self.update_post)
        self.page_edit.cancelled.connect(self.show_detail)

        self.page_new.submitted.connect(self.create_post)
        self.page_new.cancelled.connect(self.show_list)

        self.show_list()

    def show_list(self):
        self.page_list.load_posts()
        self.stack.setCurrentWidget(self.page_list)

    def show_detail(self, post_id):
        self.page_detail.load_post(post_id)
        self.stack.setCurrentWidget(self.page_detail)

    def show_edit(self, post_id):
        self.page_edit.load_post(post_id)
        self.stack.setCurrentWidget(self.page_edit)

    def show_new_post(self):
        self.stack.setCurrentWidget(self.page_new)

    def create_post(self, title, content, author):
        if not title or not content or not author:
            QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
            return
        self.db.create_post(title, content, author)
        self.show_list()

    def update_post(self, post_id, title, content):
        self.db.update_post(post_id, title, content)
        self.show_detail(post_id)

    def delete_post(self, post_id):
        reply = QMessageBox.question(self, "삭제 확인", "정말로 삭제하시겠습니까?")
        if reply == QMessageBox.Yes:
            self.db.delete_post(post_id)
            self.show_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
