from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

# Переменная для подсчета посещений
visit_count = 0

@app.route("/web")
def web():
    headers = {
        'X-Server': 'MyFlaskServer/1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'X-Developer': 'Арышева Арина Юрьевна',
        'X-Version': '1.0.0'
    }
    
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<p><a href="/author">Перейти к информации об авторе</a></p>
<p><a href="/lab1/image">Посмотреть картинку</a></p>
<p><a href="/lab1/visit">Счетчик посещений</a></p>
<p><a href="/info">Перенаправление на автора</a></p>
<p><a href="/created">Страница с кодом 201</a></p>
</body>
</html>""", 200, headers

@app.route("/web-html")
def web_html():
    # Версия с HTML content-type для нормального отображения
    headers = {
        'X-Server': 'MyFlaskServer/1.0',
        'X-Developer': 'Арышева Арина Юрьевна'
    }
    
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<p><a href="/author">Перейти к информации об авторе</a></p>
<p><a href="/lab1/image">Посмотреть картинку</a></p>
<p><a href="/lab1/visit">Счетчик посещений</a></p>
<p><a href="/info">Перенаправление на автора</a></p>
<p><a href="/created">Страница с кодом 201</a></p>
<p><a href="/web">Посмотреть версию с text/plain</a></p>
</body>
</html>""", 200, headers

@app.route("/author")
def author():
    name = "Арышева Арина Юрьевна"
    group = "ФБИ-34"
    faculty = "ФБ"
    
    return """<!doctype html>
<html>
<body>
<p>Студент: """ + name + """</p>
<p>Группа: """ + group + """</p>
<p>Факультет: """ + faculty + """</p>
<p><a href="/web-html">Вернуться на главную</a></p>
</body>
</html>"""

@app.route("/lab1/image")
def image():
    # Получаем путь к картинке и CSS с помощью url_for
    image_path = url_for('static', filename='image.jpg')
    css_path = url_for('static', filename='lab1.css')
    
    return f'''<!doctype html>
<html>
<head>
    <title>Картинка</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <div class="container">
        <h1>Моя картинка</h1>
        <div class="image-container">
            <img src="{image_path}" alt="Мое изображение">
        </div>
        <a href="/web-html" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>'''

@app.route("/lab1/visit")
def visit():
    global visit_count  # Указываем, что используем глобальную переменную
    visit_count += 1
    
    # Получаем служебную информацию
    current_time = datetime.datetime.now()
    client_ip = request.remote_addr
    server_name = request.host
    
    return """<!doctype html>
<html>
<body>
<h1>Счетчик посещений</h1>
<p>Количество посещений этой страницы: """ + str(visit_count) + """</p>
<h2>Служебная информация:</h2>
<p>Текущая дата и время: """ + str(current_time) + """</p>
<p>IP-адрес клиента: """ + client_ip + """</p>
<p>Имя хоста веб-сервера: """ + server_name + """</p>
<p><a href="/lab1/visit/reset">Очистить счетчик</a></p>
<p><a href="/web-html">Вернуться на главную</a></p>
</body>
</html>"""

@app.route("/lab1/visit/reset")
def reset_visit_counter():
    global visit_count
    visit_count = 0
    return redirect("/lab1/visit")

@app.route("/info")
def info():
    # Перенаправляем на страницу автора
    return redirect("/author")

@app.route("/created")
def created():
    # Возвращаем код 201 Created
    return "Ресурс успешно создан", 201

@app.errorhandler(404)
def page_not_found(error):
    return """<!doctype html>
<html>
<head>
    <title>Страница не найдена</title>
</head>
<body>
    <h1>Ошибка 404 - Страница не найдена</h1>
    <p>Запрашиваемая страница не существует.</p>
    <p>Пожалуйста, проверьте URL или перейдите на <a href="/web-html">главную страницу</a>.</p>
</body>
</html>""", 404