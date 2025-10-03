from flask import Flask, url_for

app = Flask(__name__)

# Главная страница
@app.route("/")
@app.route("/index")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <meta charset="utf-8">
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        
        <footer>
            <p>Арышева Арина Юрьевна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
    </html>
    """

# Страница первой лабораторной работы
@app.route("/lab1")
def lab1():
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
                <li><a href="/">Главная страница (/)</a></li>
                <li><a href="/index">Главная страница (/index)</a></li>
                <li><a href="/lab1">Первая лабораторная (/lab1)</a></li>
                <li><a href="/lab1/web">Главная страница лабораторной (/lab1/web)</a></li>
                <li><a href="/lab1/author">Информация об авторе (/lab1/author)</a></li>
                <li><a href="/lab1/image">Страница с изображением (/lab1/image)</a></li>
                <li><a href="/lab1/visit">Счетчик посещений (/lab1/visit)</a></li>
                <li><a href="/lab1/info">Перенаправление (/lab1/info)</a></li>
                <li><a href="/lab1/error">Тест ошибки 500 (/lab1/error)</a></li>
                <li><a href="/400">400 Bad Request</a></li>
                <li><a href="/401">401 Unauthorized</a></li>
                <li><a href="/402">402 Payment Required</a></li>
                <li><a href="/403">403 Forbidden</a></li>
                <li><a href="/405">405 Method Not Allowed</a></li>
                <li><a href="/418">418 I'm a teapot</a></li>
            </ul>
        </nav>

        <a href="/">Вернуться на главную страницу сайта</a>
    </body>
    </html>
    """

# Обработчики для лабораторной работы 1
@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/image")
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

@app.route("/lab1/visit")
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

@app.route("/lab1/visit/reset")
def reset_visit_counter():
    global visit_count
    visit_count = 0
    return redirect("/lab1/visit")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/error")
def server_error():
    return 10 / 0

# HTTP коды ошибок
@app.route("/400")
def bad_request():
    return "<h1>400 Bad Request</h1><p>Неверный синтаксис</p>", 400

@app.route("/401")
def unauthorized():
    return "<h1>401 Unauthorized</h1><p>Требуется аутентификация</p>", 401

@app.route("/402")
def payment_required():
    return "<h1>402 Payment Required</h1><p>Требуется оплата</p>", 402

@app.route("/403")
def forbidden():
    return "<h1>403 Forbidden</h1><p>Доступ запрещен</p>", 403

@app.route("/405")
def method_not_allowed():
    return "<h1>405 Method Not Allowed</h1><p>Метод не разрешен</p>", 405

@app.route("/418")
def im_a_teapot():
    return "<h1>418 I'm a teapot</h1><p>Я - чайник</p>", 418

@app.route("/created")
def created():
    return "Ресурс успешно создан", 201

# Обработчики ошибок
@app.errorhandler(500)
def internal_server_error(error):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ошибка 500 - Внутренняя ошибка сервера</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>500 - Ошибка сервера</h1>
        <p>Произошла внутренняя ошибка сервера</p>
        <a href="/">На главную</a> | <a href="/lab1">К лабораторной</a>
    </body>
    </html>
    """, 500

@app.errorhandler(404)
def page_not_found(error):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Страница не найдена</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>404 - Страница не найдена</h1>
        <p>Запрашиваемая страница не существует.</p>
        <a href="/">На главную</a>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)