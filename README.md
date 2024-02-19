# FastAPI SQLAlchemy Testtest

Этот проект представляет собой простое веб-приложение, созданное с использованием FastAPI и SQLAlchemy. Он предоставляет API для управления книгами и авторами в базе данных SQLite.

## Установка
1. Установите зависимости с помощью `pip`:
pip install -r requirements.txt
2. Запустите приложение:
uvicorn main:app --reload

Приложение будет доступно по адресу http://127.0.0.1:8000.

## Использование API
Для использования API, вы можете отправлять HTTP-запросы с помощью HTTP-клиента, такого как curl, Postman или другие.

### Добавление книги

Отправьте POST-запрос на /add_book с JSON-телом, содержащим информацию о книге:
http post http://127.0.0.1:8000/add_book
Content-Type: application/json

{
  "title": "Название книги",
  "author_name": "Имя автора",
  "page_count": 200
}

### Получение списка всех книг

Отправьте GET-запрос на /get_all_books:
http get http://127.0.0.1:8000/get_all_books

### Получение информации о книге по ID

Отправьте GET-запрос на /get_book/{book_id}, заменив {book_id} на фактический ID книги:
http get http://127.0.0.1:8000/get_book/1

### Удаление книги по ID

Отправьте DELETE-запрос на /delete_book/{book_id}, заменив {book_id} на фактический ID книги:
рttp delete http://127.0.0.1:8000/delete_book/1

### Добавление автора

Отправьте POST-запрос на /add_author с JSON-телом, содержащим информацию об авторе:
http post http://127.0.0.1:8000/add_author
Content-Type: application/json

{
  "name": "Имя автора"
}

### Получение информации об авторе по ID

Отправьте GET-запрос на /get_author/{author_id}, заменив {author_id} на фактический ID автора:
http get http://127.0.0.1:8000/get_author/1

### Получение списка всех авторов

Отправьте GET-запрос на /get_all_authors:
http get http://127.0.0.1:8000/get_all_authors

## Завершение работы

Для завершения работы приложения, нажмите Ctrl + C в терминале, где запущено приложение.
