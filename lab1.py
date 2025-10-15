from flask import Blueprint, url_for, request, redirect
import datetime

lab1 = Blueprint('lab1', __name__)

# Глобальная переменная для хранения лога 404 ошибок
error_404_log = []

# Страница первой лабораторной работы
@lab1.route("/")
def lab1_route():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная 1</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов

веб-приложений, сознательно предоставляющих лишь самые ба-
зовые возможности.</p>

        <h2>Список роутов</h2>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная (/lab1)</a></li>
                <li><a href="/lab1/web">Главная страница лабораторной (/lab1/web)</a></li>
                <li><a href="/lab1/author">Информация об авторе (/lab1/author)</a></li>
                <li><a href="/lab1/image">Страница с изображением (/lab1/image)</a></li>
                <li><a href="/lab1/visit">Счетчик посещений (/lab1/visit)</a></li>
                <li><a href="/lab1/info">Перенаправление (/lab1/info)</a></li>
                <li><a href="/lab1/error">Тест ошибки 500 (/lab1/error)</a></li>
            </ul>
        </nav>

        <a href="/">Вернуться на главную страницу сайта</a>
    </body>
    </html>
    """

# Обработчики для лабораторной работы 1
@lab1.route("/web")
def web():
    headers = {
        'Content-Language': 'ru',
        'X-Developer': 'Student',
        'X-Student-Group': 'FBI-34'
    }
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Главная страница лабораторной</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>web-сервер на flask</h1>
        <nav>
            <a href="/lab1/author">Автор</a> | 
            <a href="/lab1/image">Картинка</a> | 
            <a href="/lab1/visit">Счетчик</a> |
            <a href="/lab1/info">Перенаправление</a>
        </nav>
        <a href="/lab1">В меню</a> | <a href="/">На главную</a>
    </body>
    </html>
    """, 200, headers

@lab1.route("/author")
def author():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Информация об авторе</title>
        <meta charset="utf-8">
    </head>
    <body>
        <p>Студент: Арышева Арина Юрьевна</p>
        <p>Группа: ФБИ-34</p>
        <p>Факультет: ФБ</p>
        <a href="/lab1/web">Назад</a> | <a href="/">На главную</a>
    </body>
    </html>
    """

@lab1.route("/image")
def image():
    image_path = url_for('static', filename='image(2).jpg')
    headers = {
        'Content-Language': 'ru',
        'X-Developer': 'Student',
        'X-Student-Group': 'FBI-34',
        'X-Custom-Header': 'Flask-Lab-Work'
    }
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Страница с изображением</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Страница с изображением</h1>
        <img src="{image_path}" alt="Изображение" width="400">
        <br>
        <a href="/lab1/web">Назад</a> | <a href="/">На главную</a>
    </body>
    </html>
    ''', 200, headers

# Счетчик посещений
visit_count = 0

@lab1.route("/visit")
def visit():
    global visit_count
    visit_count += 1
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Счетчик посещений</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Счетчик посещений: {visit_count}</h1>
        <a href="/lab1/visit/reset">Очистить счетчик</a>
        <br>
        <a href="/lab1/web">Назад</a> | <a href="/">На главную</a>
    </body>
    </html>
    """

@lab1.route("/visit/reset")
def reset_visit_counter():
    global visit_count
    visit_count = 0
    return redirect("/lab1/visit")

@lab1.route("/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/error")
def server_error():
    return 10 / 0