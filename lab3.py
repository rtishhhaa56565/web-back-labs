from flask import Blueprint, render_template, request, make_response, redirect

# Сначала создаем Blueprint
lab3 = Blueprint('lab3', __name__)

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
            # Сбрасываем цвет
            resp = make_response(redirect('/lab3/settings'))
            resp.set_cookie('color', '', expires=0)
            return resp
    
    return render_template('lab3/settings.html')