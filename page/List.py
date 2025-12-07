class List(QWidget):
    request_new = Signal()
    request_view = Signal(int)  # post_id
    request_refresh = Signal()

    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        top_bar = QHBoxLayout()
        btn_new = QPushButton("글 작성")
        btn_new.clicked.connect(lambda: self.request_new.emit())

        btn_refresh = QPushButton("새로고침")
        btn_refresh.clicked.connect(lambda: self.request_refresh.emit())

        top_bar.addWidget(btn_new)
        top_bar.addStretch()
        top_bar.addWidget(btn_refresh)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작성자", "작성일"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self._on_double_click)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

    def refresh(self):
        posts = self.db.get_all_posts()
        self.table.setRowCount(0)
        
        for row_idx, p in enumerate(posts):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(p["id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(p["title"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(p["author"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(p["created_at"]))
        self.table.resizeColumnsToContents()

    def _on_double_click(self, row, col):
        item = self.table.item(row, 0)
        if item:
            post_id = int(item.text())
            self.request_view.emit(post_id)
