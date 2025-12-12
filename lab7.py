import sqlite3
import datetime
from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)

DB_PATH = 'database.db'


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
    cur.execute("SELECT COUNT(*) AS cnt FROM films;")
    cnt = cur.fetchone()["cnt"]
    if cnt == 0:
        seed = [
            ("Fight Club", "Бойцовский клуб", 1999, "Сотрудник страховой компании, страдающий бессонницей, встречает Тайлера Дёрдена..."),
            ("The Matrix", "Матрица", 1999, "Хакер Нео узнаёт, что реальность — симуляция..."),
            ("Gladiator", "Гладиатор", 2000, "Полководец Максимус становится гладиатором и идёт к мести..."),
            ("The Dark Knight", "Тёмный рыцарь", 2008, "Бэтмен противостоит Джокеру, который сеет хаос в Готэме..."),
            ("Parasite", "Паразиты", 2019, "Бедная семья внедряется в жизнь богатой семьи, и всё выходит из-под контроля..."),
        ]
        cur.executemany(
            "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);",
            seed
        )
        conn.commit()
    conn.close()


init_films_table()
seed_films_if_empty()


@lab7.route('/')
def main():
    return render_template('lab7/lab7.html')


def _parse_year(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_film_payload(data):
    """
    Возвращает ошибки по доп. заданию.
    """
    errors = {}

    title = str((data.get("title") or "")).strip()
    title_ru = str((data.get("title_ru") or "")).strip()
    description = str((data.get("description") or "")).strip()
    year_raw = data.get("year")

    # русское название — непустое
    if title_ru == "":
        errors["title_ru"] = "Русское название не должно быть пустым"

    # оригинальное — непустое, если русское пустое
    if title == "" and title_ru == "":
        errors["title"] = "Название (оригинал) не должно быть пустым, если русское название пустое"

    # год — 1895..текущий
    year = _parse_year(year_raw)
    current_year = datetime.datetime.now().year
    if year is None:
        errors["year"] = "Год должен быть числом"
    else:
        if year < 1895 or year > current_year:
            errors["year"] = f"Год должен быть в диапазоне 1895–{current_year}"

    # описание — непустое, <= 2000
    if description == "":
        errors["description"] = "Описание не должно быть пустым"
    elif len(description) > 2000:
        errors["description"] = "Описание не должно превышать 2000 символов"

    return errors


def ensure_exists(film_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM films WHERE id = ?;", (film_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        abort(404)


# GET /films/ — список
@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# GET /films/<id> — один
@lab7.route('/rest-api/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    ensure_exists(film_id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (film_id,))
    row = cur.fetchone()
    conn.close()
    return jsonify(dict(row))


# DELETE /films/<id>
@lab7.route('/rest-api/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    ensure_exists(film_id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM films WHERE id = ?;", (film_id,))
    conn.commit()
    conn.close()
    return ("", 204)


# PUT /films/<id>
@lab7.route('/rest-api/films/<int:film_id>', methods=['PUT'])
def edit_film(film_id):
    ensure_exists(film_id)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_film_payload(data)
    if errors:
        return jsonify(errors), 400

    title = str((data.get("title") or "")).strip()
    title_ru = str((data.get("title_ru") or "")).strip()
    year = int(data.get("year"))
    description = str((data.get("description") or "")).strip()

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


# POST /films/
@lab7.route('/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = validate_film_payload(data)
    if errors:
        return jsonify(errors), 400

    title = str((data.get("title") or "")).strip()
    title_ru = str((data.get("title_ru") or "")).strip()
    year = int(data.get("year"))
    description = str((data.get("description") or "")).strip()

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
