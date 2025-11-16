from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к БД
def get_db_connection():
    """Создание соединения с SQLite базой данных"""
    try:
        # Используем только SQLite для простоты
        dir_path = Path(__file__).parent
        db_path = dir_path / "database.db"
        conn = sqlite3.connect(db_path)
        # Установка фабрики строк для доступа по ключу
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

# Функция для закрытия подключения к БД с коммитом
def close_db_connection(conn):
    """Закрытие соединения с базой данных"""
    try:
        if conn:
            conn.commit()
            conn.close()
    except Exception as e:
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создаём таблицу статей если её нет
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    article_text TEXT NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Таблицы users и articles созданы или уже существуют")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            close_db_connection(conn)

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
        
        try:
            cursor = conn.cursor()
            
            # Проверяем, существует ли пользователь - ЗАЩИЩЕННЫЙ ЗАПРОС
            cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = "Пользователь с таким логином уже существует"
                return render_template('lab5/register.html', error=error)
            
            # Генерируем хеш пароля вместо сохранения в открытом виде
            password_hash = generate_password_hash(password)
            
            # Сохраняем хеш пароля в БД - ЗАЩИЩЕННЫЙ ЗАПРОС
            cursor.execute(
                "INSERT INTO users (login, password) VALUES (?, ?)",
                (login, password_hash)
            )
            
            print(f"Успешная регистрация: {login}")
            return redirect(url_for('lab5.success'))
            
        except Exception as e:
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/register.html', error=error)
        finally:
            close_db_connection(conn)
    
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
        
        try:
            cursor = conn.cursor()
            
            # ЗАЩИЩЕННЫЙ ЗАПРОС - параметры передаются отдельно
            cursor.execute(
                "SELECT * FROM users WHERE login = ?",
                (login,)
            )
            user = cursor.fetchone()
            
            if user:
                # Проверяем пароль с помощью check_password_hash
                if check_password_hash(user['password'], password):
                    # Сохраняем логин в сессии
                    session['username'] = login
                    session['user_id'] = user['id']
                    return redirect(url_for('lab5.success_login'))
                else:
                    error = "Неверный пароль"
            else:
                error = "Пользователь с таким логином не найден"
            
            return render_template('lab5/login.html', error=error)
                
        except Exception as e:
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/login.html', error=error)
        finally:
            close_db_connection(conn)
    
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
    session.pop('user_id', None)
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
        is_public = request.form.get('is_public') == 'on'
        
        # Проверка на пустые поля
        if not title or not article_text:
            error = "Название и текст статьи не могут быть пустыми"
            return render_template('lab5/create_article.html', error=error, username=username)
        
        conn = get_db_connection()
        if conn is None:
            error = "Ошибка подключения к базе данных"
            return render_template('lab5/create_article.html', error=error, username=username)
        
        try:
            cursor = conn.cursor()
            
            # Вставляем статью в базу данных - ЗАЩИЩЕННЫЙ ЗАПРОС
            cursor.execute(
                "INSERT INTO articles (title, article_text, user_id, is_public) VALUES (?, ?, ?, ?)",
                (title, article_text, session['user_id'], is_public)
            )
            
            return redirect(url_for('lab5.list_articles'))
            
        except Exception as e:
            error = f"Ошибка при работе с БД: {e}"
            return render_template('lab5/create_article.html', error=error, username=username)
        finally:
            close_db_connection(conn)
    
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
    
    try:
        cursor = conn.cursor()
        
        # Находим все статьи пользователя - ЗАЩИЩЕННЫЙ ЗАПРОС
        cursor.execute(
            "SELECT * FROM articles WHERE user_id = ? ORDER BY created_at DESC",
            (session['user_id'],)
        )
        articles = cursor.fetchall()
        
        return render_template('lab5/articles.html', articles=articles, username=username)
        
    except Exception as e:
        return f"Ошибка при получении статей: {e}"
    finally:
        close_db_connection(conn)

# Просмотр публичных статей
@lab5.route('/public')
def public_articles():
    conn = get_db_connection()
    if conn is None:
        return "Ошибка подключения к БД"
    
    try:
        cursor = conn.cursor()
        
        # Находим все публичные статьи - ЗАЩИЩЕННЫЙ ЗАПРОС
        cursor.execute(
            "SELECT articles.*, users.login FROM articles JOIN users ON articles.user_id = users.id WHERE articles.is_public = 1 ORDER BY articles.created_at DESC"
        )
        articles = cursor.fetchall()
        
        username = session.get('username', 'anonymous')
        return render_template('lab5/public_articles.html', articles=articles, username=username)
        
    except Exception as e:
        return f"Ошибка при получении статей: {e}"
    finally:
        close_db_connection(conn)

# Страница со списком всех пользователей (для админа)
@lab5.route('/users')
def show_users():
    conn = get_db_connection()
    if conn is None:
        return "Ошибка подключения к БД"
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, login, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        username = session.get('username', 'anonymous')
        return render_template('lab5/users.html', users=users, username=username)
        
    except Exception as e:
        return f"Ошибка при получении пользователей: {e}"
    finally:
        close_db_connection(conn)

# Тестовый маршрут для отладки
@lab5.route('/test_articles')
def test_articles():
    """Временный маршрут для тестирования"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Просто получаем все статьи - ЗАЩИЩЕННЫЙ ЗАПРОС
        cursor.execute("SELECT * FROM articles LIMIT 5")
        articles = cursor.fetchall()
        
        result = "<h1>Тест статей</h1>"
        for article in articles:
            result += f"<p>{article['id']}: {article['title']}</p>"
        
        close_db_connection(conn)
        return result
        
    except Exception as e:
        return f"Ошибка теста: {str(e)}"