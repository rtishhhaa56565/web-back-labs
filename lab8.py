from flask import Blueprint, render_template, request, redirect, session
from db.database import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

lab8 = Blueprint('lab8', __name__)

def init_tables():
    """Создаёт таблицы, если их нет. Ошибка не должна ронять приложение."""
    cur = db.cursor()
    cur.execute(users)
    cur.execute(articles)
    db.commit()

@lab8.before_request
def ensure_tables():
    # Важно: НЕ выполнять при импорте модуля.
    # Если что-то не так — не роняем весь сайт.
    try:
        init_tables()
    except sqlite3.Error:
        pass


@lab8.route('/lab8/')
def index():
    username = session.get('username', 'anonymous')
    return render_template('lab8/index.html', username=username)


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login = (request.form.get('login') or '').strip()
    password = request.form.get('password') or ''

    if not login or not password:
        return render_template('lab8/register.html', error="Введите логин и пароль.")

    cur = db.cursor()
    cur.execute("SELECT id FROM users WHERE login = ?", (login,))
    if cur.fetchone():
        return render_template('lab8/register.html', error="Такой логин уже занят.")

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password_hash))
    db.commit()

    session['username'] = login
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login = (request.form.get('login') or '').strip()
    password = request.form.get('password') or ''

    if not login or not password:
        return render_template('lab8/login.html', error="Введите логин и пароль.")

    cur = db.cursor()
    cur.execute("SELECT password FROM users WHERE login = ?", (login,))
    row = cur.fetchone()

    if not row:
        return render_template('lab8/login.html', error="Пользователь не найден.")

    # sqlite3.Row (при row_factory=sqlite3.Row) — доступ по ключу
    try:
        password_hash = row["password"]
    except Exception:
        password_hash = row[0]

    if not check_password_hash(password_hash, password):
        return render_template('lab8/login.html', error="Неверный пароль.")

    session['username'] = login
    return redirect('/lab8/')


@lab8.route('/lab8/logout')
def logout():
    session.pop('username', None)
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
def articles_list():
    return "Список статей (будет реализован позже)"


@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    return "Создание статьи (будет реализовано позже)"
