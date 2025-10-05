from flask import Flask, url_for, request, redirect, abort, render_template
import datetime

app = Flask(__name__)

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
                    <li><a href="/lab2/a">Лабораторная 2 - без слэша</a></li>
                    <li><a href="/lab2/a/">Лабораторная 2 - со слэшем</a></li>
                    <li><a href="/lab2/template">Шаблон с данными</a></li>
                    <li><a href="/lab2/template/anonymous">Шаблон анонимный</a></li>
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
                <li><a href="/lab2/a">Лабораторная 2 - без слэша</a></li>
                <li><a href="/lab2/a/">Лабораторная 2 - со слэшем</a></li>
                <li><a href="/lab2/template">Шаблон с данными</a></li>
                <li><a href="/lab2/template/anonymous">Шаблон анонимный</a></li>
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

# Обработчики для лабораторной работы 2
@app.route('/lab2/a')
def a():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная 2 - без слэша</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Обработчик без слэша</h1>
        <p>Вы находитесь на адресе: <strong>/lab2/a</strong></p>
        <p>Этот обработчик работает только для URL без завершающего слэша.</p>
        <p>Текст ответа: <strong>без слэша</strong></p>
        <nav>
            <a href="/lab2/a/">Перейти на версию со слэшем</a> | 
            <a href="/lab1">К лабораторной 1</a> | 
            <a href="/">На главную</a>
        </nav>
    </body>
    </html>
    """

@app.route('/lab2/a/')
def a2():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная 2 - со слэшем</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Обработчик со слэшем</h1>
        <p>Вы находитесь на адресе: <strong>/lab2/a/</strong></p>
        <p>Этот обработчик работает только для URL с завершающим слэшем.</p>
        <p>Текст ответа: <strong>со слэшем</strong></p>
        <nav>
            <a href="/lab2/a">Перейти на версию без слэша</a> | 
            <a href="/lab1">К лабораторной 1</a> | 
            <a href="/">На главную</a>
        </nav>
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

# Начальный список цветов
flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

# Обработчик для просмотра цветов по ID
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f"цветок: {flower_list[flower_id]}"

# Обработчик для добавления цветов
@app.route('/lab2/add_flower/<path:name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <nav>
            <a href="/lab2/flowers/0">Просмотреть цветы</a> | 
            <a href="/">На главную</a>
        </nav>
    </body>
</html>
'''

# Обработчики шаблонов с передачей переменных
@app.route("/lab2/template")
def lab2_template():
    return render_template('lab2.html', 
                         name="Арышева Арина",
                         group="ФБИ-34", 
                         course=3)

@app.route("/lab2/template/anonymous")
def lab2_template_anonymous():
    return render_template('lab2.html')

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

# Улучшенный обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    # Получаем информацию о запросе
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    # Добавляем запись в лог
    log_entry = {
        'ip': client_ip,
        'date': access_date,
        'url': requested_url
    }
    error_404_log.append(log_entry)
    
    # Формируем HTML страницы
    log_html = ""
    for entry in reversed(error_404_log[-10:]):  # Показываем последние 10 записей
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