from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

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

# Функция для закрытия подключения к БД с коммитом
def close_db_connection(conn, cursor=None):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.commit()
            conn.close()
    except Error as e:
        print(f"Ошибка при закрытии подключения: {e}")

# Функция для инициализации БД (создания таблиц)
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Создаём таблицу пользователей если её нет
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Создаём таблицу статей если её нет
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    article_text TEXT NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            cursor.close()
            print("Таблицы users и articles созданы или уже существуют")
        except Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            if conn:
                conn.close()

# Вызываем инициализацию БД при импорте
init_db()

@lab5.route('/')
def main():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

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
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Проверяем, существует ли пользователь
            cursor.execute("SELECT * FROM users WHERE login = %s;", (login,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = "Пользователь с таким логином уже существует"
                return render_template('lab5/register.html', error=error)
            
            # Генерируем хеш пароля вместо сохранения в открытом виде
            password_hash = generate_password_hash(password)
            
            # Сохраняем хеш пароля в БД
            cursor.execute(
                "INSERT INTO users (login, password) VALUES (%s, %s);",
                (login, password_hash)
            )
            
            print(f"Успешная регистрация: {login}")
            return redirect(url_for('lab5.success'))
            
        except Error as e:
            if conn:
                conn.rollback()
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/register.html', error=error)
        finally:
            close_db_connection(conn, cursor)
    
    return render_template('lab5/register.html')

# Страница успешной регистрации
@lab5.route('/success')
def success():
    return render_template('lab5/success.html')

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
        
        cursor = None
        try:
            # Используем RealDictCursor для работы с именами столбцов
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM users WHERE login = %s;",
                (login,)
            )
            user = cursor.fetchone()
            
            if user:
                # Проверяем пароль с помощью check_password_hash
                if check_password_hash(user['password'], password):
                    # Сохраняем логин в сессии
                    session['username'] = login
                    return redirect(url_for('lab5.success_login'))
                else:
                    error = "Неверный пароль"
            else:
                error = "Пользователь с таким логином не найден"
            
            return render_template('lab5/login.html', error=error)
                
        except Error as e:
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/login.html', error=error)
        finally:
            close_db_connection(conn, cursor)
    
    return render_template('lab5/login.html')

# Страница успешного входа
@lab5.route('/success_login')
def success_login():
    username = session.get('username', 'anonymous')
    return render_template('lab5/success_login.html', username=username)

# Выход из системы
@lab5.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('lab5.main'))

# Создание статьи
@lab5.route('/create', methods=['GET', 'POST'])
def create_article():
    # Проверяем аутентификацию пользователя
    username = session.get('username')
    if not username:
        return redirect(url_for('lab5.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        # Проверка на пустые поля
        if not title or not article_text:
            error = "Название и текст статьи не могут быть пустыми"
            return render_template('lab5/create_article.html', error=error, username=username)
        
        conn = get_db_connection()
        if conn is None:
            error = "Ошибка подключения к базе данных"
            return render_template('lab5/create_article.html', error=error, username=username)
        
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Находим ID пользователя
            cursor.execute("SELECT id FROM users WHERE login = %s;", (username,))
            user = cursor.fetchone()
            
            if not user:
                error = "Пользователь не найден"
                return render_template('lab5/create_article.html', error=error, username=username)
            
            # Вставляем статью в базу данных
            cursor.execute(
                "INSERT INTO articles (title, article_text, user_id) VALUES (%s, %s, %s);",
                (title, article_text, user['id'])
            )
            
            return redirect(url_for('lab5.main'))
            
        except Error as e:
            if conn:
                conn.rollback()
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/create_article.html', error=error, username=username)
        finally:
            close_db_connection(conn, cursor)
    
    return render_template('lab5/create_article.html', username=username)

# Просмотр статей пользователя
@lab5.route('/list')
def list_articles():
    # Проверяем аутентификацию пользователя
    username = session.get('username')
    if not username:
        return redirect(url_for('lab5.login'))
    
    conn = get_db_connection()
    if conn is None:
        return "Ошибка подключения к БД"
    
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Находим ID пользователя
        cursor.execute("SELECT id FROM users WHERE login = %s;", (username,))
        user = cursor.fetchone()
        
        if not user:
            return "Пользователь не найден"
        
        # Находим все статьи пользователя
        cursor.execute(
            "SELECT * FROM articles WHERE user_id = %s ORDER BY created_at DESC;",
            (user['id'],)
        )
        articles = cursor.fetchall()
        
        return render_template('lab5/articles.html', articles=articles, username=username)
        
    except Error as e:
        return f"Ошибка при получении статей: {e}"
    finally:
        close_db_connection(conn, cursor)

# Страница со списком всех пользователей (для админа)
@lab5.route('/users')
def show_users():
    conn = get_db_connection()
    if conn is None:
        return "Ошибка подключения к БД"
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, login, created_at FROM users ORDER BY created_at DESC;")
        users = cursor.fetchall()
        
        return render_template('lab5/users.html', users=users)
        
    except Error as e:
        return f"Ошибка при получении пользователей: {e}"
    finally:
        close_db_connection(conn, cursor)