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
                    <li><a href="/lab2/">Вторая лабораторная</a></li>
                    <li><a href="/lab2/a">Лабораторная 2 - без слэша</a></li>
                    <li><a href="/lab2/a/">Лабораторная 2 - со слэшем</a></li>
                    <li><a href="/lab2/template">Шаблон с данными</a></li>
                    <li><a href="/lab2/template/anonymous">Шаблон анонимный</a></li>
                    <li><a href="/lab2/flowers/all">Все цветы</a></li>
                    <li><a href="/lab2/filters">Фильтры</a></li>
                    <li><a href="/lab2/filters">Ягоды</a></li>
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

@app.route('/lab2/')
def lab2():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная работа 2</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }
            .nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }
            .nav-item {
                background: #3498db;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 10px;
                text-decoration: none;
                transition: background 0.3s ease;
            }
            .nav-item:hover {
                background: #2980b9;
            }
            .home-link {
                text-align: center;
                margin-top: 20px;
            }
            .home-link a {
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Лабораторная работа 2</h1>
            <p>Выберите раздел для просмотра:</p>
            
            <div class="nav-grid">
                <a href="/lab2/template" class="nav-item">Шаблоны</a>
                <a href="/lab2/flowers/all" class="nav-item">Цветы</a>
                <a href="/lab2/books" class="nav-item">Книги</a>
                <a href="/lab2/berries" class="nav-item">Ягоды</a>
                <a href="/lab2/filters" class="nav-item">Фильтры</a>
                <a href="/lab2/calc/" class="nav-item">Калькулятор</a>
                <a href="/lab2/a" class="nav-item">Без слэша</a>
                <a href="/lab2/a/" class="nav-item">Со слэшем</a>
            </div>
            
            <div class="home-link">
                <a href="/">← На главную страницу</a>
            </div>
        </div>
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

# Обработчик для просмотра цветов по ID с улучшенным HTML
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок #{flower_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            .flower-header {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .flower-info {{
                background: #e8f4fd;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
            }}
            .flower-details {{
                font-size: 18px;
                line-height: 1.6;
            }}
            .nav-links {{
                text-align: center;
                margin-top: 25px;
            }}
            .nav-links a {{
                display: inline-block;
                margin: 0 8px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 20px;
                transition: background 0.3s ease;
            }}
            .nav-links a:hover {{
                background: #2980b9;
            }}
            .danger {{
                background: #e74c3c !important;
            }}
            .danger:hover {{
                background: #c0392b !important;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="flower-header">
                <h1>Информация о цветке</h1>
            </div>
            
            <div class="flower-info">
                <div class="flower-details">
                    <p><strong>ID цветка:</strong> {flower_id}</p>
                    <p><strong>Название:</strong> {flower_list[flower_id]}</p>
                    <p><strong>Всего цветов в коллекции:</strong> {len(flower_list)}</p>
                </div>
            </div>
            
            <div class="nav-links">
                <a href="/lab2/flowers/all">Все цветы</a>
                <a href="/lab2/add_flower/новый_цветок">Добавить цветок</a>
                <a href="/lab2/flowers/clear" class="danger">Очистить список</a>
                <a href="/">На главную</a>
            </div>
        </div>
    </body>
</html>
'''

# Обработчик для очистки списка цветов
@app.route('/lab2/flowers/clear')
def clear_flowers():
    global flower_list
    flower_list.clear()
    flower_list.extend(['роза', 'тюльпан', 'незабудка', 'ромашка'])  # Восстанавливаем начальные
    return '''
<!doctype html>
<html>
    <head>
        <title>Список очищен</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .success-message {{
                background: #e8f6f3;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 25px;
                border-left: 5px solid #27ae60;
            }}
            .nav-links {{
                margin-top: 25px;
            }}
            .nav-links a {{
                display: inline-block;
                margin: 0 8px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 20px;
                transition: background 0.3s ease;
            }}
            .nav-links a:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-message">
                <h1>Список цветов очищен!</h1>
                <p>Все цветы были удалены из коллекции.</p>
                <p><strong>Восстановлены начальные цветы:</strong> роза, тюльпан, незабудка, ромашка</p>
            </div>
            
            <div class="nav-links">
                <a href="/lab2/flowers/all">Посмотреть все цветы</a>
                <a href="/lab2/add_flower/орхидея">Добавить новый цветок</a>
                <a href="/">На главную</a>
            </div>
        </div>
    </body>
</html>
'''

# Список фруктов
fruits = [
    {'name': 'яблоки', 'price': 100},
    {'name': 'груши', 'price': 120},
    {'name': 'апельсины', 'price': 80},
    {'name': 'мандарины', 'price': 95},
    {'name': 'манго', 'price': 321}
]

# Обработчики шаблонов с передачей переменных
@app.route("/lab2/template")
def lab2_template():
    return render_template('example.html', 
                         name="Арышева Арина",
                         group="ФБИ-34", 
                         course=3,
                         fruits=fruits)

@app.route("/lab2/template/anonymous")
def lab2_template_anonymous():
    return render_template('example.html', fruits=fruits)

# Обработчик для страницы фильтров
@app.route('/lab2/filters')
def filters():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Фильтры</title>
    </head>
    <body>
        <h1>Фильтры Jinja2</h1>
        <p>Фраза: О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...</p>
    </body>
    </html>
    """
# Обработчики для калькулятора с переадресацией
@app.route('/lab2/calc/')
def calc_default():
    """Переадресация на /lab2/calc/1/1 по умолчанию"""
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single_number(a):
    """Переадресация с одного числа на два числа (второе = 1)"""
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc_two_numbers(a, b):
    """Обработчик для двух чисел - математические операции"""
    try:
        # Выполняем математические операции
        addition = a + b
        subtraction = a - b
        multiplication = a * b
        division = a / b if b != 0 else "Ошибка: деление на ноль"
        exponentiation = a ** b
        
        return f'''
<!doctype html>
<html>
    <head>
        <title>Калькулятор</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            h1 {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .numbers {{
                background: #e8f4fd;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }}
            .operations {{
                margin-top: 20px;
            }}
            .operation {{
                padding: 10px;
                margin: 8px 0;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #3498db;
            }}
            .nav-links {{
                text-align: center;
                margin-top: 25px;
            }}
            .nav-links a {{
                display: inline-block;
                margin: 0 8px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 20px;
            }}
            .nav-links a:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Калькулятор</h1>
            
            <div class="numbers">
                <h2>Исходные числа:</h2>
                <p><strong>Первое число (a):</strong> {a}</p>
                <p><strong>Второе число (b):</strong> {b}</p>
            </div>
            
            <div class="operations">
                <h2>Результаты операций:</h2>
                <div class="operation">
                    <strong>Суммирование:</strong> {a} + {b} = {addition}
                </div>
                <div class="operation">
                    <strong>Вычитание:</strong> {a} - {b} = {subtraction}
                </div>
                <div class="operation">
                    <strong>Умножение:</strong> {a} × {b} = {multiplication}
                </div>
                <div class="operation">
                    <strong>Деление:</strong> {a} ÷ {b} = {division}
                </div>
                <div class="operation">
                    <strong>Возведение в степень:</strong> {a}<sup>{b}</sup> = {exponentiation}
                </div>
            </div>
            
            <div class="nav-links">
                <a href="/lab2/calc/10/5">Пример: 10 и 5</a>
                <a href="/lab2/calc/8/2">Пример: 8 и 2</a>
                <a href="/lab2/calc/15/3">Пример: 15 и 3</a>
                <a href="/">На главную</a>
            </div>
        </div>
    </body>
</html>
'''
    except Exception as e:
        return f"Ошибка: {str(e)}", 500
    
# Список книг
books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 320},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 576},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 128},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

# Обработчик для вывода списка книг
@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

# Список ягод
berries = [
    {
        'name': 'Клубника', 
        'description': 'Сладкая красная ягода с сочной мякотью, богатая витамином C',
        'image': 'images_yagody/strawberry.jpg'
    },
    {
        'name': 'Малина', 
        'description': 'Ароматная ягода с нежной текстурой, используется в десертах и варенье',
        'image': 'images_yagody/raspberry.jpg'
    },
    {
        'name': 'Черника', 
        'description': 'Маленькая синяя ягода, полезна для зрения и памяти',
        'image': 'images_yagody/blueberry.jpg'
    },
    {
        'name': 'Ежевика', 
        'description': 'Тёмная ягода с кисло-сладким вкусом, растёт на колючих кустах',
        'image': 'images_yagody/blackberry.jpg'
    },
    {
        'name': 'Смородина красная', 
        'description': 'Прозрачная красная ягода с освежающим кисловатым вкусом',
        'image': 'images_yagody/red_currant.jpg'
    },
    {
        'name': 'Смородина чёрная', 
        'description': 'Ароматная тёмная ягода с высоким содержанием витаминов',
        'image': 'images_yagody/black_currant.jpg'
    },
    {
        'name': 'Крыжовник', 
        'description': 'Зелёная или красная ягода с полосами, используется в компотах',
        'image': 'images_yagody/gooseberry.jpg'
    },
    {
        'name': 'Земляника', 
        'description': 'Лесная ягода с интенсивным ароматом, мельче садовой клубники',
        'image': 'images_yagody/wild_strawberry.jpg'
    },
    {
        'name': 'Брусника', 
        'description': 'Красная горьковатая ягода, часто используется в мочёном виде',
        'image': 'images_yagody/lingonberry.jpg'
    },
    {
        'name': 'Клюква', 
        'description': 'Кислая красная ягода, растёт на болотах, богата антиоксидантами',
        'image': 'images_yagody/cranberry.jpg'
    },
    {
        'name': 'Голубика', 
        'description': 'Крупная синяя ягода с белым налётом, похожа на чернику',
        'image': 'images_yagody/bilberry.jpg'
    },
    {
        'name': 'Облепиха', 
        'description': 'Оранжевая ягода с кислым вкусом, очень богата витаминами',
        'image': 'images_yagody/sea_buckthorn.jpg'
    },
    {
        'name': 'Шиповник', 
        'description': 'Плоды розы, используются для витаминных чаёв и отваров',
        'image': 'images_yagody/rosehip.jpg'
    },
    {
        'name': 'Рябина', 
        'description': 'Красные горькие ягоды, становятся сладкими после заморозков',
        'image': 'images_yagody/rowan.jpg'
    },
    {
        'name': 'Калина', 
        'description': 'Красные ягоды с горьким вкусом, используются в народной медицине',
        'image': 'images_yagody/viburnum.jpg'
    },
    {
        'name': 'Ирга', 
        'description': 'Сладкие синие ягоды, похожи на чернику, но более крупные',
        'image': 'images_yagody/serviceberry.jpg'
    },
    {
        'name': 'Жимолость', 
        'description': 'Синие продолговатые ягоды с уникальным вкусом, созревают рано',
        'image': 'images_yagody/honeysuckle.jpg'
    },
    {
        'name': 'Боярышник', 
        'description': 'Красные мучнистые ягоды, полезны для сердечно-сосудистой системы',
        'image': 'images_yagody/hawthorn.jpg'
    },
    {
        'name': 'Бузина', 
        'description': 'Чёрные мелкие ягоды, используются в медицине и кулинарии',
        'image': 'images_yagody/elderberry.jpg'
    },
    {
        'name': 'Виноград', 
        'description': 'Сочные ягоды разного цвета, используются для еды и виноделия',
        'image': 'images_yagody/grape.jpg'
    }
]

# Обработчик для отображения ягод
@app.route('/lab2/berries')
def berries_list():
    return render_template('berries.html', berries=berries)

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