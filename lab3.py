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