<div align="center">

# 📝 PySide6 Desktop Bulletin Board

**PySide6 + SQLite 기반 데스크톱 게시판 프로그램**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green)
![SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

</div>

---

## 📌 소개 (Introduction)

PySide6(Qt for Python)으로 만든 **데스크톱 게시판 CRUD 애플리케이션**입니다.  
SQLite 데이터베이스를 사용해 게시글을 저장하며,  
QStackedWidget 기반 페이지 전환과 Signal/Slot 구조를 활용한 깔끔한 아키텍처로 구성되어 있습니다.

---

## 🛠 사용 기술 (Tech Stack)

### **Frontend / UI**

- Python 3.10+
- PySide6 (Qt Widgets)
- QStackedWidget 페이지 전환
- Signal/Slot 구조 이벤트 처리

### **Backend**

- SQLite3 (파일 기반 RDBMS)
- SQL 직접 작성 (ORM 미사용)

---

## 📁 프로젝트 구조 (Project Structure)

````bash
project/
│── main.py                 # 프로그램 진입점
│── board.db                # SQLite DB 파일 (자동 생성)
│── venv/                   # Python 가상환경
│── README.md
│
└── src/
    ├── db/
    │   └── db_manager.py   # SQLite CRUD 관리
    │
    ├── pages/              # 화면 구성
    │   ├── page_list.py    # 목록 페이지
    │   ├── page_detail.py  # 상세보기 페이지
    │   ├── page_new.py     # 새 글 작성 페이지
    │   └── page_edit.py    # 수정 페이지
    │
    └── core/
        └── router.py       # 페이지 전환 로직


## ✨ 주요 기능 (Features)

- ✔ ** 게시글 목록 조회 ** (QTableWidget)
- ✔ ** 게시글 작성 ** (Create)
- ✔ ** 게시글 조회 ** (Read)
- ✔ ** 게시글 수정 ** (Update)
- ✔ ** 게시글 삭제 ** (Delete)
- ✔ ** SQLite 기반 데이터 저장 **
- ✔ ** QStackedWidget 기반 페이지 이동 **
- ✔ ** Signal / Slot 기반 이벤트 처리 **
- ✔ ** 입력값 검증 ** (제목/내용 비어 있을 시 저장 불가)
- ✔ ** 삭제 전 사용자 확인 ** (QMessageBox)


---

## 💾 데이터베이스 구조 (SQLite Schema)

```sql
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
````
