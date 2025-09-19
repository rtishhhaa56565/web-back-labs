from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

# Переменная для подсчета посещений
visit_count = 0

@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
<html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
    </header>
    
    <main>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/http-codes">HTTP коды ответов</a></li>
            </ul>
        </nav>
    </main>
    
    <footer>
        <p>Арышева Арина Юрьевна, ФБИ-34, 3 курс, 2025</p>
    </footer>
</body>
</html>"""

@app.route("/http-codes")
def http_codes():
    return """<!doctype html>
<html>
<head>
    <title>HTTP коды ответов</title>
</head>
<body>
    <h1>Тестовые HTTP коды ответов</h1>
    <nav>
        <ul>
            <li><a href="/400">400 Bad Request</a></li>
            <li><a href="/401">401 Unauthorized</a></li>
            <li><a href="/402">402 Payment Required</a></li>
            <li><a href="/403">403 Forbidden</a></li>
            <li><a href="/405">405 Method Not Allowed</a></li>
            <li><a href="/418">418 I'm a teapot</a></li>
        </ul>
    </nav>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>"""

@app.route("/400")
def bad_request():
    return """<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 400

@app.route("/401")
def unauthorized():
    return """<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 401

@app.route("/402")
def payment_required():
    return """<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Запрос не может быть обработан until the client makes a payment.</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 402

@app.route("/403")
def forbidden():
    return """<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к запрашиваемому ресурсу запрещен.</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 403

@app.route("/405")
def method_not_allowed():
    return """<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Метод, указанный в запросе, не разрешен для данного ресурса.</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 405

@app.route("/418")
def im_a_teapot():
    return """<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>Я - чайник. Не могу заварить кофе.</p>
    <p>Это шуточный код из RFC 2324 (Hyper Text Coffee Pot Control Protocol).</p>
    <p><a href="/http-codes">Вернуться к списку кодов</a></p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 418

@app.route("/lab1")
def lab1_index():
    return """<!doctype html>
<html>
<head>
    <title>Лабораторная 1</title>
</head>
<body>
    <h1>Лабораторная работа 1</h1>
    
    <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов

веб-приложений, сознательно предоставляющих лишь самые ба-
зовые возможности.</p>

    <nav>
        <ul>
            <li><a href="/lab1/web-html">Главная страница лабораторной</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Страница с картинкой</a></li>
            <li><a href="/lab1/visit">Счетчик посещений</a></li>
            <li><a href="/lab1/info">Перенаправление</a></li>
        </ul>
    </nav>

    <p><a href="/">Вернуться на главную страницу сайта</a></p>
</body>
</html>"""

# ... остальные существующие обработчики (web, web-html, author, image, visit, info, created) ...

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
    <p>Пожалуйста, проверьте URL или перейдите на <a href="/">главную страницу</a>.</p>
</body>
</html>""", 404