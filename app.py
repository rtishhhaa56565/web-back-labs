from flask import Flask, url_for, request
import datetime

app = Flask(__name__)

# Переменная для подсчета посещений
visit_count = 0

@app.route("/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<p><a href="/author">Перейти к информации об авторе</a></p>
<p><a href="/lab1/image">Посмотреть картинку</a></p>
<p><a href="/lab1/visit">Счетчик посещений</a></p>
</body>
</html>"""

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
<p><a href="/web">Вернуться на главную</a></p>
</body>
</html>"""

@app.route("/lab1/image")
def image():
    # Получаем путь к картинке с помощью url_for
    image_path = url_for('static', filename='image.jpg')
    
    return '''<!doctype html>
<html>
<head>
    <title>Картинка</title>
</head>
<body>
    <h1>Моя картинка</h1>
    <img src="''' + image_path + '''" alt="Мое изображение" width="500">
    <p><a href="/web">Вернуться на главную</a></p>
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
<p><a href="/web">Вернуться на главную</a></p>
</body>
</html>"""