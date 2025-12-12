import sqlite3
import datetime
from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)


@lab7.route('/')
def main():
    return render_template('lab7/lab7.html')


# ---------- DB helpers ----------

DB_PATH = 'database.db'  # лежит рядом с app.py

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_films_table():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def seed_films_if_empty():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM films;")
    cnt = cur.fetchone()["cnt"]
    if cnt == 0:
        films_seed = [
            ("Fight Club", "Бойцовский клуб", 1999, "Сотрудник страховой компании, страдающий бессонницей, встречает Тайлера Дёрдена..."),
            ("The Matrix", "Матрица", 1999, "Хакер Нео узнаёт, что реальность — симуляция..."),
            ("Gladiator", "Гладиатор", 2000, "Полководец Максимус становится гладиатором и идёт к мести..."),
            ("The Dark Knight", "Тёмный рыцарь", 2008, "Бэтмен противостоит Джокеру, который сеет хаос в Готэме..."),
            ("Parasite", "Паразиты", 2019, "Бедная семья внедряется в жизнь богатой семьи, и всё выходит из-под контроля..."),
        ]
        cur.executemany(
            "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);",
            films_seed
        )
        conn.commit()
    conn.close()


# Инициализируем БД при первом импорте модуля
init_films_table()
seed_films_if_empty()


# ---------- Validation ----------

def _parse_year(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_film_payload(data):
    """
    Возвращает dict ошибок вида:
    {
      "title_ru": "...",
      "title": "...",
      "year": "...",
      "description": "..."
    }
    Если ошибок нет — пустой dict.
    """
    errors = {}
    title = (data.get("title") if data else "") or ""
    title_ru = (data.get("title_ru") if data else "") or ""
    description = (data.get("description") if data else "") or ""
    year_raw = data.get("year") if data else None

    title = str(title).strip()
    title_ru = str(title_ru).strip()
    description = str(description).strip()

    # Русское название — должно быть непустым (по методичке)
    if title_ru == "":
        errors["title_ru"] = "Русское название не должно быть пустым"

    # Оригинальное название — должно быть непустым, если русское пустое
    # (формально этот пункт при обязательном title_ru почти никогда не сработает,
    # но оставим как требование)
    if title == "" and title_ru == "":
        errors["title"] = "Название (оригинал) не должно быть пустым, если русское название пустое"

    # Год — от 1895 до текущего
    year = _parse_year(year_raw)
    current_year = datetime.datetime.now().year
    if year is None:
        errors["year"] = "Год должен быть числом"
    else:
        if year < 1895 or year > current_year:
            errors["year"] = f"Год должен быть в диапазоне 1895–{current_year}"

    # Описание — непустое, не более 2000 символов
    if description == "":
        errors["description"] = "Описание не должно быть пустым"
    elif len(description) > 2000:
        errors["description"] = "Описание не должно превышать 2000 символов"

    return errors


def _validate_id_exists(film_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM films WHERE id = ?;", (film_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        abort(404)


# ---------- REST API ----------

@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    films = [dict(r) for r in rows]
    return jsonify(films)


@lab7.route('/rest-api/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    _validate_id_exists(film_id)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (film_id,))
    row = cur.fetchone()
    conn.close()
    return jsonify(dict(row))


@lab7.route('/rest-api/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    _validate_id_exists(film_id)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM films WHERE id = ?;", (film_id,))
    conn.commit()
    conn.close()
    return ("", 204)


@lab7.route('/rest-api/films/<int:film_id>', methods=['PUT'])
def edit_film(film_id):
    _validate_id_exists(film_id)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_film_payload(data)
    if errors:
        return jsonify(errors), 400

    title = (data.get("title") or "").strip()
    title_ru = (data.get("title_ru") or "").strip()
    year = int(data.get("year"))
    description = (data.get("description") or "").strip()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE films
           SET title = ?, title_ru = ?, year = ?, description = ?
         WHERE id = ?;
    """, (title, title_ru, year, description, film_id))
    conn.commit()

    cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (film_id,))
    row = cur.fetchone()
    conn.close()

    return jsonify(dict(row))


@lab7.route('/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_film_payload(data)
    if errors:
        return jsonify(errors), 400

    title = (data.get("title") or "").strip()
    title_ru = (data.get("title_ru") or "").strip()
    year = int(data.get("year"))
    description = (data.get("description") or "").strip()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);",
        (title, title_ru, year, description)
    )
    conn.commit()
    new_id = cur.lastrowid

    conn.close()
    return jsonify({"id": new_id}), 201
