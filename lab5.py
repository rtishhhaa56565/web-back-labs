from flask import Blueprint, render_template, request, redirect, url_for

lab5 = Blueprint('lab5', __name__)

@lab5.route('/')
def main():
    return render_template('lab5/lab5.html', username="anonymous")

@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        # Проверка на пустые поля
        if not login or not password:
            error = "Логин и пароль не могут быть пустыми"
            return render_template('lab5/register.html', error=error)
        
        # Здесь будет логика сохранения в БД
        print(f"Регистрация: {login}, {password}")  # Для тестирования
        return redirect('/lab5')
    
    return render_template('lab5/register.html')