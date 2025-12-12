from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5 
from lab6 import lab6  
from lab7 import lab7  

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_12345'

# 🔹 ВАЖНО: корректное отображение кириллицы в JSON
app.config['JSON_AS_ASCII'] = False

# Чтение секретного ключа из переменной окружения SECRET_KEY
# Если переменной нет, используется значение по умолчанию
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'секретно-секретный-секрет'
)

# Чтение типа базы данных из переменной окружения DB_TYPE
# Если переменной нет, используется значение по умолчанию 'postgres'
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

# Регистрация blueprint'ов
app.register_blueprint(lab1, url_prefix='/lab1')
app.register_blueprint(lab2, url_prefix='/lab2')
app.register_blueprint(lab3, url_prefix='/lab3')
app.register_blueprint(lab4, url_prefix='/lab4')
app.register_blueprint(lab5, url_prefix='/lab5')
app.register_blueprint(lab6, url_prefix='/lab6')
app.register_blueprint(lab7, url_prefix='/lab7')

# Глобальная переменная для хранения лога 404 ошибок
error_404_log = []

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
                    <li><a href="/lab2/">Вторая лабораторная</a></li>
                    <li><a href="/lab3/">Третья лабораторная</a></li>
                    <li><a href="/lab4/">Четвертая лабораторная</a></li>
                    <li><a href="/lab5/">Пятая лабораторная</a></li>
                    <li><a href="/lab6/">Шестая лабораторная</a></li>
                    <li><a href="/lab7/">Седьмая лабораторная (REST API)</a></li>
                    <li><a href="/lab2/a">Лабораторная 2 - без слэша</a></li>
                    <li><a href="/lab2/a/">Лабораторная 2 - со слэшем</a></li>
                    <li><a href="/lab2/template">Шаблон с данными</a></li>
                    <li><a href="/lab2/template/anonymous">Шаблон анонимный</a></li>
                    <li><a href="/lab2/flowers/all">Все цветы</a></li>
                    <li><a href="/lab2/filters">Фильтры</a></li>
                    <li><a href="/lab2/berries">Ягоды</a></li>
                </ul>
            </nav>
        </main>

        <footer>
            <p>Арышева Арина Юрьевна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
    </html>
    """

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicons/favicon.ico')

@app.route('/test-favicons')
def test_favicons():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Тест фавиконок</title>
    </head>
    <body>
        <h1>Тест доступности фавиконок</h1>
        <ul>
            <li><a href="/static/favicons/favicon.ico">favicon.ico</a></li>
            <li><a href="/static/favicons/favicon-16x16.png">favicon-16x16.png</a></li>
            <li><a href="/static/favicons/favicon-32x32.png">favicon-32x32.png</a></li>
        </ul>
    </body>
    </html>
    """

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

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_server_error(error):
    return """
    <h1>500 - Ошибка сервера</h1>
    <p>Произошла внутренняя ошибка сервера</p>
    <a href="/">На главную</a>
    """, 500

# Улучшенный обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url

    error_404_log.append({
        'ip': client_ip,
        'date': access_date,
        'url': requested_url
    })

    log_html = ""
    for entry in reversed(error_404_log[-10:]):
        log_html += (
            f"<tr><td>{entry['ip']}</td>"
            f"<td>{entry['date']}</td>"
            f"<td>{entry['url']}</td></tr>"
        )

    return f"""
    <h1>404 — Страница не найдена</h1>
    <p><b>URL:</b> {requested_url}</p>
    <table border="1">
        <tr><th>IP</th><th>Дата</th><th>URL</th></tr>
        {log_html}
    </table>
    """, 404


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
