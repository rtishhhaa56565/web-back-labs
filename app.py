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
    <p>Для доaccess к запрашиваемому ресурсу требуется аутентификация.</p>
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

# Обработчик, который вызывает ошибку на сервере
@app.route("/error-test")
def error_test():
    # Вызываем ошибку деления на ноль
    result = 10 / 0  # Это вызовет ZeroDivisionError
    return "Эта строка никогда не будет показана"

# Альтернативный вариант с конкатенацией числа и строки
@app.route("/error-test2")
def error_test2():
    number = 42
    text = "текст"
    result = number + text  # Это вызовет TypeError
    return result

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_server_error(error):
    return """<!doctype html>
<html>
<head>
    <title>500 - Ошибка сервера</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: #f8f9fa;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #dc3545; 
            margin-bottom: 20px;
        }
        .error-code {
            font-size: 48px;
            font-weight: bold;
            color: #dc3545;
            margin-bottom: 10px;
        }
        p {
            margin: 15px 0;
            line-height: 1.6;
        }
        .btn {
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #0056b3;
        }
        .technical-info {
            margin-top: 30px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            font-size: 14px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">500</div>
        <h1>Внутренняя ошибка сервера</h1>
        
        <p>На сервере произошла непредвиденная ошибка. Приносим извинения за неудобства.</p>
        <p>Наша команда уже уведомлена о проблеме и работает над её решением.</p>
        
        <div>
            <a href="/" class="btn">Вернуться на главную</a>
            <a href="javascript:history.back()" class="btn">Назад</a>
        </div>
        
        <div class="technical-info">
            <strong>Техническая информация:</strong><br>
            Произошла ошибка во время обработки вашего запроса.<br>
            Время: {current_time}<br>
            Ошибка: {error_type}
        </div>
    </div>
</body>
</html>""".format(
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        error_type=type(error).__name__
    ), 500

@app.errorhandler(404)
def page_not_found(error):
    return """<!doctype html>
<html>
<head>
    <title>404</title>
    <style>
        body { 
            font-family: Arial; 
            text-align: center; 
            padding: 50px; 
            background: #f8f9fa;
        }
        h1 { color: #dc3545; }
        img { width: 300px; height: auto; margin: 20px; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>404 - Страница не найдена</h1>
    <img src="/static/images (3).jpg" alt="Ошибка">
    <p>Такой страницы не существует.</p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>""", 404
@app.route("/lab1/image")
def image():
    # Получаем путь к картинке и CSS с помощью url_for
    image_path = url_for('static', filename='image.jpg')
    css_path = url_for('static', filename='lab1.css')
    
    # Кастомные заголовки
    headers = {
        'Content-Language': 'ru',  # Язык контента - русский
        'X-Image-Processor': 'Flask-Image-Service/1.0',
        'X-Custom-Header': 'Специальный заголовок для лабораторной работы',
        'X-Student-Info': 'Арышева Арина Юрьевна, ФБИ-34'
    }
    
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
        <a href="/lab1/web-html" class="back-link">Вернуться к первой лабораторной</a>
        <a href="/lab1" class="back-link">Вернуться к меню лабораторной</a>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>''', 200, headers

