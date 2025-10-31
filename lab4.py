from flask import Blueprint, render_template, request, redirect, url_for, session

lab4 = Blueprint('lab4', __name__)

@lab4.route('/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/div', methods=['GET', 'POST'])
def div():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        
        if not x1 or not x2:
            return render_template('lab4/div-result.html', error="Оба поля должны быть заполнены")
        
        try:
            x1 = float(x1)
            x2 = float(x2)
            
            if x2 == 0:
                return render_template('lab4/div-result.html', error="Деление на ноль невозможно")
            
            result = x1 / x2
            return render_template('lab4/div-result.html', x1=x1, x2=x2, result=result)
            
        except ValueError:
            return render_template('lab4/div-result.html', error="Введите корректные числа")
    
    return render_template('lab4/div-form.html')

@lab4.route('/sum', methods=['GET', 'POST'])
def sum_numbers():
    if request.method == 'POST':
        x1 = request.form.get('x1', '0')
        x2 = request.form.get('x2', '0')
        
        try:
            x1 = float(x1) if x1 else 0
            x2 = float(x2) if x2 else 0
            result = x1 + x2
            return render_template('lab4/sum-result.html', x1=x1, x2=x2, result=result)
        except ValueError:
            return render_template('lab4/sum-result.html', error="Введите корректные числа")
    
    return render_template('lab4/sum-form.html')

@lab4.route('/multiply', methods=['GET', 'POST'])
def multiply():
    if request.method == 'POST':
        x1 = request.form.get('x1', '1')
        x2 = request.form.get('x2', '1')
        
        try:
            x1 = float(x1) if x1 else 1
            x2 = float(x2) if x2 else 1
            result = x1 * x2
            return render_template('lab4/multiply-result.html', x1=x1, x2=x2, result=result)
        except ValueError:
            return render_template('lab4/multiply-result.html', error="Введите корректные числа")
    
    return render_template('lab4/multiply-form.html')

@lab4.route('/subtract', methods=['GET', 'POST'])
def subtract():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        
        if not x1 or not x2:
            return render_template('lab4/subtract-result.html', error="Оба поля должны быть заполнены")
        
        try:
            x1 = float(x1)
            x2 = float(x2)
            result = x1 - x2
            return render_template('lab4/subtract-result.html', x1=x1, x2=x2, result=result)
        except ValueError:
            return render_template('lab4/subtract-result.html', error="Введите корректные числа")
    
    return render_template('lab4/subtract-form.html')

@lab4.route('/power', methods=['GET', 'POST'])
def power():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        
        if not x1 or not x2:
            return render_template('lab4/power-result.html', error="Оба поля должны быть заполнены")
        
        try:
            x1 = float(x1)
            x2 = float(x2)
            
            if x1 == 0 and x2 == 0:
                return render_template('lab4/power-result.html', error="Ноль в нулевой степени не определен")
            
            result = x1 ** x2
            return render_template('lab4/power-result.html', x1=x1, x2=x2, result=result)
        except ValueError:
            return render_template('lab4/power-result.html', error="Введите корректные числа")
    
    return render_template('lab4/power-form.html')

# Глобальная переменная для хранения количества деревьев
tree_count = 0

@lab4.route('/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'plant' and tree_count < 10:  # Максимум 10 деревьев
            tree_count += 1
        elif operation == 'cut' and tree_count > 0:   # Минимум 0 деревьев
            tree_count -= 1
        
        # После обработки POST делаем редирект на GET-запрос
        return redirect(url_for('lab4.tree'))
    
    # GET-запрос - просто отображаем страницу
    return render_template('lab4/tree.html', tree_count=tree_count)

# Расширенный список пользователей (логин: {данные})
users = {
    'arina': {
        'password': '123',
        'name': 'Арышева Арина',
        'gender': 'женский'
    },
    'user': {
        'password': '456', 
        'name': 'Мария Сидорова',
        'gender': 'женский'
    },
    'admin': {
        'password': 'admin',
        'name': 'Администратор Системы',
        'gender': 'мужской'
    },
    'test': {
        'password': 'test',
        'name': 'Тестовый Пользователь',
        'gender': 'женский'
    }
}

@lab4.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'cancel':
            session.pop('username', None)
            return redirect(url_for('lab4.login'))
        
        elif action == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Проверка на пустые значения
            if not username:
                return render_template('lab4/login.html', 
                                    error='Не введён логин', 
                                    username=username)
            
            if not password:
                return render_template('lab4/login.html', 
                                    error='Не введён пароль', 
                                    username=username)
            
            # Проверка логина и пароля
            if username in users and users[username]['password'] == password:
                session['username'] = username
                return redirect(url_for('lab4.login'))
            else:
                return render_template('lab4/login.html', 
                                    error='Неверные логин и/или пароль', 
                                    username=username)
        
        elif action == 'register':
            return redirect(url_for('lab4.register'))
    
    # GET-запрос
    username = session.get('username')
    if username:
        user_data = users.get(username, {})
        return render_template('lab4/login-success.html', 
                             username=user_data.get('name', username))
    else:
        return render_template('lab4/login.html')

@lab4.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'cancel':
            return redirect(url_for('lab4.login'))
        
        elif action == 'register':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            full_name = request.form.get('full_name')
            gender = request.form.get('gender')
            
            # Валидация данных
            if not username:
                return render_template('lab4/register.html', error='Не введён логин')
            
            if not password:
                return render_template('lab4/register.html', error='Не введён пароль')
            
            if not full_name:
                return render_template('lab4/register.html', error='Не введено имя')
            
            if password != confirm_password:
                return render_template('lab4/register.html', error='Пароли не совпадают')
            
            if username in users:
                return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')
            
            if len(username) < 3:
                return render_template('lab4/register.html', error='Логин должен содержать минимум 3 символа')
            
            if len(password) < 3:
                return render_template('lab4/register.html', error='Пароль должен содержать минимум 3 символа')
            
            # Регистрация нового пользователя с расширенными данными
            users[username] = {
                'password': password,
                'name': full_name,
                'gender': gender
            }
            return render_template('lab4/register-success.html', username=full_name)
    
    return render_template('lab4/register.html')

@lab4.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('lab4.login'))

@lab4.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['lang'] = request.form.get('lang', 'ru')
        session['theme'] = request.form.get('theme', 'light')
        return redirect(url_for('lab4.settings'))
    
    current_lang = session.get('lang', 'ru')
    current_theme = session.get('theme', 'light')
    
    return render_template('lab4/settings.html', 
                         current_lang=current_lang, 
                         current_theme=current_theme)

@lab4.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('lab4.login'))
    
    user_data = users.get(username, {})
    lang = session.get('lang', 'ru')
    theme = session.get('theme', 'light')
    
    return render_template('lab4/profile.html', 
                         username=user_data.get('name', username),
                         user_data=user_data,
                         lang=lang,
                         theme=theme)

@lab4.route('/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        temperature = request.form.get('temperature')
        
        # Проверка на пустое значение
        if not temperature:
            return render_template('lab4/fridge-result.html', 
                                error='Ошибка: не задана температура')
        
        try:
            temp = float(temperature)
            
            # Проверка диапазонов температуры
            if temp < -12:
                return render_template('lab4/fridge-result.html', 
                                    error='Не удалось установить температуру — слишком низкое значение')
            elif temp > -1:
                return render_template('lab4/fridge-result.html', 
                                    error='Не удалось установить температуру — слишком высокое значение')
            elif -12 <= temp <= -9:
                snowflakes = 3
                message = f'Установлена температура: {temp}°C'
            elif -8 <= temp <= -5:
                snowflakes = 2
                message = f'Установлена температура: {temp}°C'
            elif -4 <= temp <= -1:
                snowflakes = 1
                message = f'Установлена температура: {temp}°C'
            else:
                snowflakes = 0
                message = f'Установлена температура: {temp}°C'
            
            return render_template('lab4/fridge-result.html', 
                                message=message, 
                                snowflakes=snowflakes,
                                temperature=temp)
            
        except ValueError:
            return render_template('lab4/fridge-result.html', 
                                error='Ошибка: введите корректное число')
    
    return render_template('lab4/fridge-form.html')

@lab4.route('/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')
        
        # Проверка на пустые значения
        if not grain_type:
            return render_template('lab4/grain-result.html', 
                                error='Ошибка: не выбран тип зерна')
        
        if not weight:
            return render_template('lab4/grain-result.html', 
                                error='Ошибка: не указан вес')
        
        try:
            weight_float = float(weight)
            
            # Проверка на неположительный вес
            if weight_float <= 0:
                return render_template('lab4/grain-result.html', 
                                    error='Ошибка: вес должен быть больше 0')
            
            # Проверка на слишком большой объем
            if weight_float > 100:
                return render_template('lab4/grain-result.html', 
                                    error='Извините, такого объёма сейчас нет в наличии')
            
            # Цены за тонну
            prices = {
                'barley': 12000,  # ячмень
                'oats': 8500,     # овёс
                'wheat': 9000,    # пшеница
                'rye': 15000      # рожь
            }
            
            # Названия зерна
            grain_names = {
                'barley': 'ячмень',
                'oats': 'овёс', 
                'wheat': 'пшеница',
                'rye': 'рожь'
            }
            
            # Расчет стоимости
            base_price = prices[grain_type]
            total = weight_float * base_price
            
            # Применение скидки
            discount = 0
            if weight_float > 10:
                discount = total * 0.10
                total -= discount
            
            grain_name = grain_names[grain_type]
            
            return render_template('lab4/grain-result.html', 
                                grain_name=grain_name,
                                weight=weight_float,
                                total=total,
                                discount=discount,
                                has_discount=weight_float > 10)
            
        except ValueError:
            return render_template('lab4/grain-result.html', 
                                error='Ошибка: введите корректный вес')
    
    return render_template('lab4/grain-form.html')