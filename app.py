from flask import Flask, url_for

app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<p><a href="/author">Перейти к информации об авторе</a></p>
<p><a href="/lab1/image">Посмотреть картинку</a></p>
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