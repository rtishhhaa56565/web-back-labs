from flask import Blueprint, render_template, request, redirect, url_for

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