class Write(QWidget):
    saved = Signal()
    canceled = Signal()

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("제목")
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("작성자")
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("내용")

        btn_bar = QHBoxLayout()
        btn_save = QPushButton("저장")
        btn_cancel = QPushButton("취소")
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(lambda: self.canceled.emit())

        btn_bar.addStretch()
        btn_bar.addWidget(btn_save)
        btn_bar.addWidget(btn_cancel)

        layout.addWidget(QLabel("제목"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("작성자"))
        layout.addWidget(self.author_edit)
        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_edit)
        layout.addLayout(btn_bar)

    def save(self):
        title = self.title_edit.text().strip()
        author = self.author_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
 
        #유효성 검사
        if not title or not content:
            QMessageBox.warning(self, "작성 실패", "제목과 내용을 작성해주세요.")
            return
        self.db.create_post(title, content, author or "익명")
        QMessageBox.information(self, "완료", "저장되었습니다.")
 
        # 입력창 비운 후 저장
        self.title_edit.clear()
        self.author_edit.clear()
        self.content_edit.clear()
        self.saved.emit()
