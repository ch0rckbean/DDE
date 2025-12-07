class Read(QWidget):
    request_edit = Signal(int)    # 수정
    request_delete = Signal(int)  # 삭제 
    back_to_list = Signal()       # 목록 이동 

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self.current_id = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.title_label = QLabel()   
        self.meta_label = QLabel()    
        self.content_label = QLabel() 
        self.content_label.setWordWrap(True)

        
        btn_bar = QHBoxLayout()
        btn_edit = QPushButton("수정")
        btn_delete = QPushButton("삭제")
        btn_back = QPushButton("목록으로")

        btn_edit.clicked.connect(lambda: self.request_edit.emit(self.current_id))
        btn_delete.clicked.connect(self._on_delete)
        btn_back.clicked.connect(lambda: self.back_to_list.emit())

        btn_bar.addWidget(btn_edit)
        btn_bar.addWidget(btn_delete)
        btn_bar.addStretch()
        btn_bar.addWidget(btn_back)

        layout.addWidget(self.title_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.content_label)
        layout.addLayout(btn_bar)

    # 게시물 로드
    def load_post(self, post_id: int):
        post = self.db.get_post(post_id)
        if not post:
            QMessageBox.warning(self, "오류", "게시물을 찾을 수 없습니다.")
            self.back_to_list.emit()
            return

        self.current_id = post_id
        self.title_label.setText(f"<h2>{post['title']}</h2>")
        self.meta_label.setText(f"작성자: {post['author']} | 작성일: {post['created_at']}")
        self.content_label.setText(post['content'])

    def _on_delete(self):
        confirm = QMessageBox.question(self, "삭제 확인", "정말 삭제하시겠습니까?")
        if confirm == QMessageBox.Yes and self.current_id is not None:
            self.db.delete_post(self.current_id)
            QMessageBox.information(self, "삭제", "게시글이 삭제되었습니다.")
            self.back_to_list.emit()

