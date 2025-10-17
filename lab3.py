from flask import Blueprint, render_template, request, make_response, redirect

# Сначала создаем Blueprint
lab3 = Blueprint('lab3', __name__)

# Список товаров 
products = [
    {'name': 'iPhone 15 Pro', 'price': 99990, 'brand': 'Apple', 'color': 'Титановый синий', 'storage': '128GB'},
    {'name': 'Samsung Galaxy S24', 'price': 79990, 'brand': 'Samsung', 'color': 'Чёрный', 'storage': '256GB'},
    {'name': 'Xiaomi 14', 'price': 59990, 'brand': 'Xiaomi', 'color': 'Белый', 'storage': '256GB'},
    {'name': 'Google Pixel 8', 'price': 69990, 'brand': 'Google', 'color': 'Зелёный', 'storage': '128GB'},
    {'name': 'OnePlus 12', 'price': 64990, 'brand': 'OnePlus', 'color': 'Чёрный', 'storage': '256GB'},
    {'name': 'iPhone 14', 'price': 74990, 'brand': 'Apple', 'color': 'Фиолетовый', 'storage': '128GB'},
    {'name': 'Samsung Galaxy A54', 'price': 34990, 'brand': 'Samsung', 'color': 'Синий', 'storage': '128GB'},
    {'name': 'Xiaomi Redmi Note 13', 'price': 24990, 'brand': 'Xiaomi', 'color': 'Чёрный', 'storage': '128GB'},
    {'name': 'Realme 11 Pro', 'price': 29990, 'brand': 'Realme', 'color': 'Золотой', 'storage': '256GB'},
    {'name': 'Nothing Phone 2', 'price': 45990, 'brand': 'Nothing', 'color': 'Белый', 'storage': '256GB'},
    {'name': 'iPhone SE', 'price': 44990, 'brand': 'Apple', 'color': 'Красный', 'storage': '64GB'},
    {'name': 'Samsung Galaxy Z Flip5', 'price': 89990, 'brand': 'Samsung', 'color': 'Фиолетовый', 'storage': '256GB'},
    {'name': 'Google Pixel 7a', 'price': 44990, 'brand': 'Google', 'color': 'Белый', 'storage': '128GB'},
    {'name': 'Xiaomi Poco X6', 'price': 27990, 'brand': 'Xiaomi', 'color': 'Синий', 'storage': '256GB'},
    {'name': 'OnePlus Nord 3', 'price': 37990, 'brand': 'OnePlus', 'color': 'Зелёный', 'storage': '256GB'},
    {'name': 'iPhone 15', 'price': 84990, 'brand': 'Apple', 'color': 'Розовый', 'storage': '128GB'},
    {'name': 'Samsung Galaxy S23 FE', 'price': 54990, 'brand': 'Samsung', 'color': 'Кремовый', 'storage': '128GB'},
    {'name': 'Xiaomi 13T', 'price': 49990, 'brand': 'Xiaomi', 'color': 'Чёрный', 'storage': '256GB'},
    {'name': 'Motorola Edge 40', 'price': 42990, 'brand': 'Motorola', 'color': 'Синий', 'storage': '256GB'},
    {'name': 'Honor 90', 'price': 34990, 'brand': 'Honor', 'color': 'Изумрудный', 'storage': '256GB'},
    {'name': 'iPhone 13', 'price': 59990, 'brand': 'Apple', 'color': 'Синий', 'storage': '128GB'},
    {'name': 'Samsung Galaxy A34', 'price': 29990, 'brand': 'Samsung', 'color': 'Серебристый', 'storage': '128GB'},
    {'name': 'Xiaomi Redmi 12', 'price': 17990, 'brand': 'Xiaomi', 'color': 'Чёрный', 'storage': '128GB'},
    {'name': 'Realme Narzo 60', 'price': 19990, 'brand': 'Realme', 'color': 'Оранжевый', 'storage': '128GB'},
    {'name': 'Nokia G42', 'price': 15990, 'brand': 'Nokia', 'color': 'Фиолетовый', 'storage': '128GB'}
]

# Затем используем декораторы
@lab3.route('/')
def lab():
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)

@lab3.route('/cookie')
def cookie():
    resp = make_response('установка cookie')
    resp.set_cookie('name', 'Alex')
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')
    return resp

@lab3.route('/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('color', '', expires=0)
    return resp

@lab3.route('/form1', methods=['GET', 'POST'])
def form1():
    errors = {}
    user = ''
    age = ''
    gender = ''

    if request.method == 'POST':
        user = request.form.get('user', '').strip()
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')

        # Проверка имени пользователя
        if not user:
            errors['user'] = 'Заполните поле имени'
        elif len(user) < 2:
            errors['user'] = 'Имя должно содержать минимум 2 символа'
        elif len(user) > 50:
            errors['user'] = 'Имя не должно превышать 50 символов'

        # Проверка возраста
        if age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом'

    else:  # GET запрос
        user = request.args.get('user', '')
        age = request.args.get('age', '')
        gender = request.args.get('gender', '')

    return render_template('lab3/form1.html', 
                         user=user, age=age, gender=gender, 
                         errors=errors)

# НОВЫЕ ОБРАБОТЧИКИ ДЛЯ ЗАКАЗА НАПИТКА
@lab3.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        drink = request.form.get('drink')
        sugar = 'sugar' in request.form
        milk = 'milk' in request.form
        
        price = 0
        if drink == 'coffee':
            price = 200
        elif drink in ['black-tea', 'green-tea']:
            price = 150
            
        if sugar:
            price += 10
        if milk:
            price += 20
            
        return render_template('lab3/pay.html', 
                             drink=drink, sugar=sugar, milk=milk, 
                             price=price)
    
    return render_template('lab3/order.html')

@lab3.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        drink = request.form.get('drink')
        sugar = 'sugar' in request.form
        milk = 'milk' in request.form
        
        price = 0
        if drink == 'coffee':
            price = 200
        elif drink in ['black-tea', 'green-tea']:
            price = 150
            
        if sugar:
            price += 10
        if milk:
            price += 20
            
        return render_template('lab3/pay.html', 
                             drink=drink, sugar=sugar, milk=milk, 
                             price=price)
    
    return render_template('lab3/pay.html')

@lab3.route('/success', methods=['POST'])
def success():
    drink = request.form.get('drink')
    sugar = 'sugar' in request.form
    milk = 'milk' in request.form
    price = request.form.get('price')
    
    return render_template('lab3/success.html',
                         drink=drink, sugar=sugar, milk=milk,
                         price=price)

@lab3.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'set':
            # Получаем цвет из формы
            color = request.form.get('color_text') or request.form.get('color')
            if color:
                resp = make_response(redirect('/lab3/settings'))
                resp.set_cookie('color', color)
                return resp
        
        elif action == 'clear':
            # Сбрасываем ВСЕ куки, установленные в settings
            resp = make_response(redirect('/lab3/settings'))
            
            # Очищаем все куки, которые могут быть установлены в lab3
            cookies_to_clear = [
                'color',                    # цвет текста
                'products_min_price',       # минимальная цена товаров
                'products_max_price',       # максимальная цена товаров
                'name', 'age', 'color'      # куки из других обработчиков
            ]
            
            for cookie_name in cookies_to_clear:
                resp.set_cookie(cookie_name, '', expires=0)
            
            return resp
    
    return render_template('lab3/settings.html')

@lab3.route('/ticket', methods=['GET', 'POST'])
def ticket():
    errors = []
    
    if request.method == 'POST':
        # Получаем данные из формы
        fio = request.form.get('fio', '').strip()
        age_str = request.form.get('age', '').strip()
        shelf = request.form.get('shelf', '')
        linen = 'linen' in request.form
        luggage = 'luggage' in request.form
        insurance = 'insurance' in request.form
        departure = request.form.get('departure', '').strip()
        destination = request.form.get('destination', '').strip()
        date = request.form.get('date', '')
        
        # Валидация
        if not fio:
            errors.append('Заполните ФИО пассажира')
        
        if not age_str:
            errors.append('Заполните возраст')
        else:
            try:
                age = int(age_str)
                if age < 1 or age > 120:
                    errors.append('Возраст должен быть от 1 до 120 лет')
            except ValueError:
                errors.append('Возраст должен быть числом')
        
        if not shelf:
            errors.append('Выберите полку')
        
        if not departure:
            errors.append('Заполните пункт выезда')
        
        if not destination:
            errors.append('Заполните пункт назначения')
        
        if not date:
            errors.append('Выберите дату поездки')
        
        # Если нет ошибок - рассчитываем стоимость и показываем результат
        if not errors:
            age = int(age_str)
            is_child = age < 18
            
            # Расчет стоимости
            base_price = 700 if is_child else 1000
            
            shelf_price = 100 if shelf in ['lower', 'side_lower'] else 0
            linen_price = 75 if linen else 0
            luggage_price = 250 if luggage else 0
            insurance_price = 150 if insurance else 0
            
            total_price = base_price + shelf_price + linen_price + luggage_price + insurance_price
            
            return render_template('lab3/ticket_result.html',
                                 fio=fio,
                                 age=age,
                                 is_child=is_child,
                                 shelf=shelf,
                                 linen=linen,
                                 luggage=luggage,
                                 insurance=insurance,
                                 departure=departure,
                                 destination=destination,
                                 date=date,
                                 base_price=base_price,
                                 shelf_price=shelf_price,
                                 linen_price=linen_price,
                                 luggage_price=luggage_price,
                                 insurance_price=insurance_price,
                                 total_price=total_price)
        
        # Если есть ошибки - показываем форму снова
        return render_template('lab3/ticket.html',
                             errors=errors,
                             fio=fio,
                             age=age_str,
                             shelf=shelf,
                             linen=linen,
                             luggage=luggage,
                             insurance=insurance,
                             departure=departure,
                             destination=destination,
                             date=date)
    
    # GET запрос - показываем пустую форму
    return render_template('lab3/ticket.html')

@lab3.route('/products', methods=['GET', 'POST'])
def products_search():
    # Получаем минимальную и максимальную цены из всех товаров
    min_product_price = min(product['price'] for product in products)
    max_product_price = max(product['price'] for product in products)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'search':
            # Получаем значения из формы
            min_price_str = request.form.get('min_price', '').strip()
            max_price_str = request.form.get('max_price', '').strip()
            
            # Преобразуем в числа, если не пустые
            min_price = int(min_price_str) if min_price_str else None
            max_price = int(max_price_str) if max_price_str else None
            
            # Если пользователь перепутал min и max - меняем местами
            if min_price is not None and max_price is not None and min_price > max_price:
                min_price, max_price = max_price, min_price
            
            # Фильтруем товары
            filtered_products = []
            for product in products:
                price = product['price']
                # Проверяем условия фильтрации
                price_match = True
                
                if min_price is not None and price < min_price:
                    price_match = False
                if max_price is not None and price > max_price:
                    price_match = False
                
                if price_match:
                    filtered_products.append(product)
            
            # Сохраняем значения в куки
            resp = make_response(render_template('lab3/products.html',
                                               all_products=products,
                                               filtered_products=filtered_products,
                                               min_price=min_price,
                                               max_price=max_price,
                                               min_product_price=min_product_price,
                                               max_product_price=max_product_price,
                                               search_range={'min_price': min_price, 'max_price': max_price}))
            
            # Сохраняем в куки
            if min_price is not None:
                resp.set_cookie('products_min_price', str(min_price))
            if max_price is not None:
                resp.set_cookie('products_max_price', str(max_price))
            
            return resp
        
        elif action == 'reset':
            # Сбрасываем фильтры и куки
            resp = make_response(render_template('lab3/products.html',
                                               all_products=products,
                                               min_product_price=min_product_price,
                                               max_product_price=max_product_price))
            
            # Очищаем куки
            resp.set_cookie('products_min_price', '', expires=0)
            resp.set_cookie('products_max_price', '', expires=0)
            
            return resp
    
    else:  # GET запрос
        # Пытаемся получить значения из куки
        min_price_cookie = request.cookies.get('products_min_price')
        max_price_cookie = request.cookies.get('products_max_price')
        
        min_price = int(min_price_cookie) if min_price_cookie else None
        max_price = int(max_price_cookie) if max_price_cookie else None
        
        if min_price is not None or max_price is not None:
            # Фильтруем товары по значениям из куки
            filtered_products = []
            for product in products:
                price = product['price']
                price_match = True
                
                if min_price is not None and price < min_price:
                    price_match = False
                if max_price is not None and price > max_price:
                    price_match = False
                
                if price_match:
                    filtered_products.append(product)
            
            return render_template('lab3/products.html',
                                 all_products=products,
                                 filtered_products=filtered_products,
                                 min_price=min_price,
                                 max_price=max_price,
                                 min_product_price=min_product_price,
                                 max_product_price=max_product_price,
                                 search_range={'min_price': min_price, 'max_price': max_price})
        
        else:
            # Показываем все товары
            return render_template('lab3/products.html',
                                 all_products=products,
                                 min_product_price=min_product_price,
                                 max_product_price=max_product_price)