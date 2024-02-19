from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import List

Base = declarative_base()

'''Определение модели для таблицы "authors" с указанием столбцов  '''
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    books = relationship("Book", back_populates="author")

'''Определение модели для таблицы "books" с указанием столбцов  '''
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    page_count = Column(Integer)
    author = relationship("Author", back_populates="books")

'''Модель входных данных для создания книги'''
class BookCreate(BaseModel):
    title: str
    author_name: str
    page_count: int

'''Модель входных данных для создания автора'''
class AuthorCreate(BaseModel):
    name: str

'''URL для подключения к базе данных SQLite'''
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

'''Очистка и создание таблиц при каждом новом запуске, при необходимости сохранения всех
внесенных записей в БД, очистку при каждом новом запуске можно убрать'''
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

'''Настройка сессии SQLAlchemy'''
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

'''Функция получения id автора по его имени'''
def get_author_id(db, author_name):
    author = db.query(Author).filter(Author.name == author_name).first()
    if not author:
        new_author = Author(name=author_name)
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return new_author.id
    return author.id

'''Метод для добавления новой книги'''
@app.post("/add_book")
def add_book(book: BookCreate):
    try:
        db = SessionLocal()
        author_id = get_author_id(db, book.author_name)
        db_book = Book(title=book.title, author_id=author_id, page_count=book.page_count)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        db.close()
        return {"message": "Книга добавлена успешно!", "book_id": db_book.id, "author": book.author_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод для получения информации о всех книгах добавленных в БД'''
@app.get("/get_all_books", response_model=List[dict])
def get_all_books():
    try:
        db = SessionLocal()
        books = db.query(Book.id, Book.title, Book.page_count, Author.name.label("author")).join(Author).all()
        db.close()
        return [{"id": book.id, "title": book.title, "author": book.author, "page_count": book.page_count} for book in
                books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод для получения информации о всех авторах добавленных в БД'''
@app.get("/get_all_authors", response_model=List[dict])
def get_all_authors():
    try:
        db = SessionLocal()
        authors = db.query(Author.id, Author.name).all()
        db.close()
        return [{"id": author.id, "name": author.name} for author in
                authors]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод для удаления книги по ее id'''
@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int):
    try:
        db = SessionLocal()
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        db.delete(book)
        db.commit()
        db.close()
        return {"message": "Книга успешно удалена", "deleted_book_id": book_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод для полочения информации о книге по ее id'''
@app.get("/get_book/{book_id}", response_model=dict)
def get_book(book_id: int):
    try:
        db = SessionLocal()
        book = db.query(Book.id, Book.title, Book.page_count, Author.name.label("author")).join(Author).filter(
            Book.id == book_id).first()
        db.close()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return {"id": book.id, "title": book.title, "author": book.author, "page_count": book.page_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод ля добавления нового автора'''
@app.post("/add_author")
def add_author(author: AuthorCreate):
    try:
        db = SessionLocal()
        new_author = Author(name=author.name)
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        db.close()
        return {"message": "Автор добавлен успешно!", "author_id": new_author.id, "author_name": new_author.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

'''Метод для получения информации об авторе и его книгах по введеному id'''
@app.get("/get_author/{author_id}", response_model=dict)
def get_author(author_id: int):
    try:
        db = SessionLocal()
        author = db.query(Author).filter(Author.id == author_id).first()
        books = db.query(Book).filter(Book.author_id == author_id).all()
        db.close()
        if not author:
            raise HTTPException(status_code=404, detail="Автор не найден")
        return {"id": author.id, "name": author.name,
                "books": [{"id": book.id, "title": book.title, "page_count": book.page_count} for book in books]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
