from flask import Blueprint, render_template, request

lab4 = Blueprint('lab4', __name__)

@lab4.route('/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/div', methods=['GET', 'POST'])
def div():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        # Здесь будет обработка деления
        return f"Результат: {x1} / {x2}"
    return render_template('lab4/div-form.html')  