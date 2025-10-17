from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime

lab2 = Blueprint('lab2', __name__)

# Обновленный список цветов с ID и ценами
flower_list = [
    {'id': 1, 'name': 'роза', 'price': 300},
    {'id': 2, 'name': 'тюльпан', 'price': 310},
    {'id': 3, 'name': 'незабудка', 'price': 320},
    {'id': 4, 'name': 'ромашка', 'price': 330},
    {'id': 5, 'name': 'георгин', 'price': 300},
    {'id': 6, 'name': 'гладиолус', 'price': 310}
]

# Список фруктов
fruits = [
    {'name': 'яблоки', 'price': 100},
    {'name': 'груши', 'price': 120},
    {'name': 'апельсины', 'price': 80},
    {'name': 'мандарины', 'price': 95},
    {'name': 'манго', 'price': 321}
]

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
        'description': 'Сочные ягоды разного цвета, используются для еда и виноделия',
        'image': 'images_yagody/grape.jpg'
    }
]

# Главная страница лабораторной работы 2
@lab2.route("/")
def lab2_route():
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

# Обработчики для лабораторной работы 2
@lab2.route("/a")
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

@lab2.route("/a/")
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

# Обработчик для вывода всех цветов с шаблоном
@lab2.route("/flowers/all")
def all_flowers():
    total_price = sum(flower['price'] for flower in flower_list)
    return render_template('lab2/flowers_all.html', 
                         flowers=flower_list,
                         total_price=total_price)

# Обработчик для добавления цветка (форма)
@lab2.route("/flowers/add", methods=['POST'])
def add_flower():
    name = request.form.get('flower_name')
    if name:
        # Находим максимальный ID и добавляем новый
        max_id = max(flower['id'] for flower in flower_list) if flower_list else 0
        new_flower = {
            'id': max_id + 1,
            'name': name,
            'price': 300  # цена по умолчанию
        }
        flower_list.append(new_flower)
    return redirect('/lab2/flowers/all')

# Обработчик для удаления цветка по номеру
@lab2.route("/flowers/delete/<int:flower_id>")
def delete_flower(flower_id):
    # Ищем цветок по ID
    flower_to_delete = None
    for flower in flower_list:
        if flower['id'] == flower_id:
            flower_to_delete = flower
            break
    
    # Если цветок не найден - возвращаем 404
    if flower_to_delete is None:
        abort(404)
    
    # Удаляем цветок из списка
    flower_list.remove(flower_to_delete)
    return redirect('/lab2/flowers/all')

# Обработчик для удаления всех цветов
@lab2.route("/flowers/delete_all")
def delete_all_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/all')

# Обработчики шаблонов с передачей переменных
@lab2.route("/template")
def lab2_template():
    return render_template('lab2/example.html', 
                         name="Арышева Арина",
                         group="ФБИ-34", 
                         course=3,
                         fruits=fruits)

@lab2.route("/template/anonymous")
def lab2_template_anonymous():
    return render_template('lab2/example.html', fruits=fruits)

# Обработчик для страницы фильтров
@lab2.route("/filters")
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
@lab2.route("/calc/")
def calc_default():
    """Переадресация на /lab2/calc/1/1 по умолчанию"""
    return redirect('/lab2/calc/1/1')

@lab2.route("/calc/<int:a>")
def calc_single_number(a):
    """Переадресация с одного числа на два числа (второе = 1)"""
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route("/calc/<int:a>/<int:b>")
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

# Обработчик для вывода списка книг
@lab2.route("/books")
def books_list():
    return render_template('lab2/books.html', books=books)

# Обработчик для отображения ягод
@lab2.route("/berries")
def berries_list():
    return render_template('lab2/berries.html', berries=berries)