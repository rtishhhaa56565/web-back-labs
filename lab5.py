from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import Error

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к БД
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",           
            database="web_lab5",     
            user="arina_arysheva_knowledge_base",            
            password="secure_password_123"    
        )
        return conn
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

# Функция для инициализации БД (создания таблицы)
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cursor.close()
            print("Таблица users создана или уже существует")
        except Error as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            conn.close()

# Вызываем инициализацию БД при импорте
init_db()

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
        
        # Подключение к БД и проверка существования пользователя
        conn = get_db_connection()
        if conn is None:
            error = "Ошибка подключения к базе данных"
            return render_template('lab5/register.html', error=error)
        
        try:
            cursor = conn.cursor()
            
            # Проверяем, существует ли пользователь
            cursor.execute("SELECT * FROM users WHERE login = %s;", (login,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = "Пользователь с таким логином уже существует"
                cursor.close()
                conn.close()
                return render_template('lab5/register.html', error=error)
            
            # Если пользователя нет - сохраняем в БД
            cursor.execute(
                "INSERT INTO users (login, password) VALUES (%s, %s);",
                (login, password)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Успешная регистрация: {login}")
            return redirect(url_for('lab5.success'))
            
        except Error as e:
            conn.rollback()
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/register.html', error=error)
        finally:
            if conn:
                conn.close()
    
    return render_template('lab5/register.html')

# Новая страница для успешной регистрации
@lab5.route('/success')
def success():
    return render_template('lab5/success.html')

# Дополнительные маршруты:

# Страница входа
@lab5.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        if not login or not password:
            error = "Логин и пароль не могут быть пустыми"
            return render_template('lab5/login.html', error=error)
        
        conn = get_db_connection()
        if conn is None:
            error = "Ошибка подключения к базе данных"
            return render_template('lab5/login.html', error=error)
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE login = %s AND password = %s;",
                (login, password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                return redirect(url_for('lab5.main'))
            else:
                error = "Неверный логин или пароль"
                return render_template('lab5/login.html', error=error)
                
        except Error as e:
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/login.html', error=error)
        finally:
            if conn:
                conn.close()
    
    return render_template('lab5/login.html')

# Страница со списком всех пользователей (для админа)
@lab5.route('/users')
def show_users():
    conn = get_db_connection()
    if conn is None:
        return "Ошибка подключения к БД"
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, login, created_at FROM users ORDER BY created_at DESC;")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('lab5/users.html', users=users)
        
    except Error as e:
        return f"Ошибка при получении пользователей: {e}"
    finally:
        if conn:
            conn.close()