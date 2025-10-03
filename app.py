from flask import Flask, url_for

app = Flask(__name__)

# Главная страница
@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Главная страница</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Тестирование ошибки 500 и заголовков</h1>
        <ul>
            <li><a href="/error1">Ошибка 1: Деление на ноль</a></li>
            <li><a href="/error2">Ошибка 2: Конкатенация числа и строки</a></li>
            <li><a href="/image">Страница с изображением (тест заголовков)</a></li>
        </ul>
    </body>
    </html>
    """

# Обработчики, вызывающие ошибки
@app.route("/error1")
def error1():
    # Деление на ноль
    result = 10 / 0
    return "Эта строка никогда не выполнится"

@app.route("/error2")
def error2():
    # Конкатенация числа и строки
    number = 42
    text = "текст"
    result = number + text  # TypeError
    return str(result)

# Обработчик /image с кастомными заголовками
@app.route("/image")
def image():
    # Кастомные заголовки - значения только на латинице
    headers = {
        'Content-Language': 'ru',
        'X-Developer': 'Student',
        'X-Student-Group': 'FBI-34',
        'X-Custom-Header': 'Flask-Lab-Work'
    }
    
    image_path = url_for('static', filename='image(2).jpg')
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Страница с изображением</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }}
            .image-container {{
                margin: 20px auto;
            }}
            .image-container img {{
                max-width: 100%;
                height: auto;
                border: 2px solid #333;
                border-radius: 10px;
            }}
            .info {{
                margin-top: 20px;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 5px;
                text-align: left;
            }}
            .header-list {{
                background: white;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Тестирование кастомных заголовков ответа</h1>
        
        <div class="image-container">
            <img src="{image_path}" alt="Тестовое изображение" width="400">
        </div>
        
        <div class="info">
            <h3>Кастомные заголовки этого ответа:</h3>
            
            <div class="header-list">
                <strong>Content-Language: ru</strong><br>
                <em>Назначение:</em> Указывает язык контента страницы<br>
                <em>Возможные значения:</em> ru (русский), en (английский), fr (французский) и т.д.
            </div>
            
            <div class="header-list">
                <strong>X-Developer: Student</strong><br>
                <em>Назначение:</em> Кастомный заголовок с информацией о разработчике
            </div>
            
            <div class="header-list">
                <strong>X-Student-Group: FBI-34</strong><br>
                <em>Назначение:</em> Кастомный заголовок с учебной группой
            </div>

            <div class="header-list">
                <strong>X-Custom-Header: Flask-Lab-Work</strong><br>
                <em>Назначение:</em> Произвольный кастомный заголовок
            </div>
            
            <h4>Как проверить заголовки:</h4>
            <ol>
                <li>Откройте Инструменты разработчика (F12)</li>
                <li>Перейдите на вкладку "Network"</li>
                <li>Обновите страницу (Ctrl+R)</li>
                <li>Кликните на запрос "image"</li>
                <li>Перейдите на вкладку "Headers"</li>
                <li>В разделе "Response Headers" увидите все заголовки</li>
            </ol>
        </div>
        
        <a href="/">Вернуться на главную</a>
    </body>
    </html>
    ''', 200, headers

# Обработчик ошибки 500 (внутренняя ошибка сервера)
@app.errorhandler(500)
def internal_server_error(error):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ошибка 500 - Внутренняя ошибка сервера</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .error-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            .error-code {
                font-size: 72px;
                color: #d32f2f;
                margin: 0;
            }
            .error-title {
                color: #333;
                margin-bottom: 20px;
            }
            .error-message {
                color: #666;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .home-link {
                display: inline-block;
                padding: 10px 20px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .home-link:hover {
                background: #1976D2;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1 class="error-code">500</h1>
            <h2 class="error-title">Внутренняя ошибка сервера</h2>
            <p class="error-message">
                На сервере произошла непредвиденная ошибка. Приносим извинения за неудобства.
                Наша команда уже уведомлена о проблеме и работает над её решением.
            </p>
            <p class="error-message">
                Пожалуйста, попробуйте обновить страницу через несколько минут или вернуться на главную страницу.
            </p>
            <a href="/" class="home-link">Вернуться на главную страницу</a>
        </div>
    </body>
    </html>
    """, 500

# Обработчик ошибки 404
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
    # Запуск без режима отладки для работы обработчика 500
    app.run(debug=False, host='127.0.0.1', port=5000)