from flask import Flask, request
import datetime
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

# Корректное отображение кириллицы в JSON
app.config['JSON_AS_ASCII'] = False
try:
    app.json.ensure_ascii = False
except Exception:
    pass

# Ключ для сессий (достаточно одного способа)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')

# (опционально) тип БД
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

# ✅ Регистрируем blueprint'ы БЕЗ url_prefix,
# потому что префиксы уже зашиты внутри labX.py (например, /lab9/)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

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
                    <li><a href="/lab8/">Восьмая лабораторная</a></li>
                    <li><a href="/lab9/">Девятая лабораторная</a></li>

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

        <h2>Проверка ссылок:</h2>
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
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url

    error_404_log.append({'ip': client_ip, 'date': access_date, 'url': requested_url})

    log_html = ""
    for entry in reversed(error_404_log[-10:]):
        log_html += f"<tr><td>{entry['ip']}</td><td>{entry['date']}</td><td>{entry['url']}</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Страница не найдена - Ошибка 404</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .error-container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .error-code {{
                font-size: 72px;
                color: #d32f2f;
                margin: 0;
                text-align: center;
            }}
            .error-title {{
                color: #333;
                margin-bottom: 20px;
                text-align: center;
            }}
            .info-section {{
                background: #e8f4fd;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .log-section {{
                background: white;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .home-link {{
                display: inline-block;
                padding: 10px 20px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1 class="error-code">404</h1>
            <h2 class="error-title">Страница не найдена</h2>

            <div class="info-section">
                <h3>Информация о запросе:</h3>
                <p><strong>IP-адрес пользователя:</strong> {client_ip}</p>
                <p><strong>Дата и время доступа:</strong> {access_date}</p>
                <p><strong>Запрошенный URL:</strong> {requested_url}</p>
            </div>

            <p>Запрашиваемая страница не существует. Пожалуйста, проверьте URL или перейдите на главную страницу.</p>

            <a href="/" class="home-link">Перейти на главную страницу</a>
        </div>

        <div class="log-section">
            <h3>Лог 404 ошибок (последние 10 записей):</h3>
            <table>
                <thead>
                    <tr>
                        <th>IP-адрес</th>
                        <th>Дата и время</th>
                        <th>Запрошенный URL</th>
                    </tr>
                </thead>
                <tbody>
                    {log_html}
                </tbody>
            </table>
            <p style="margin-top: 10px; font-size: 12px; color: #666;">
                Всего записей в логе: {len(error_404_log)}
            </p>
        </div>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
