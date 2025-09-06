from flask import Flask
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-сервер на flask</h1>
<p><a href="/author">Перейти к информации об авторе</a></p>
</body>
</html>"""

@app.route("/author")
def author():
    name = "Иванов Иван Иванович"
    group = "ФБИ-80"
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