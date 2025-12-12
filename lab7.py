from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)


@lab7.route('/')
def main():
    # шаблон: templates/lab7/lab7.html
    return render_template('lab7/lab7.html')


# Список фильмов (хранится в памяти)
films = [
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": (
            "Сотрудник страховой компании, страдающий хронической бессонницей, "
            "встречает харизматичного торговца мылом Тайлера Дёрдена. Вместе они "
            "создают подпольный бойцовский клуб, который со временем перерастает "
            "в опасное движение, выходящее из-под контроля."
        )
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": (
            "Хакер по имени Нео узнаёт, что реальность, в которой живёт человечество, "
            "является всего лишь иллюзией, созданной машинами. Он присоединяется "
            "к группе повстанцев, чтобы раскрыть правду и освободить людей из "
            "виртуального плена."
        )
    },
    {
        "title": "Gladiator",
        "title_ru": "Гладиатор",
        "year": 2000,
        "description": (
            "Римский полководец Максимус, преданный и лишённый семьи, становится "
            "гладиатором. Он проходит путь от раба до символа надежды для народа, "
            "стремясь отомстить императору, разрушившему его жизнь."
        )
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": (
            "Бэтмен сталкивается с новым врагом — Джокером, гениальным преступником, "
            "сеющим хаос в Готэме. Противостояние превращается в борьбу не только "
            "за город, но и за моральные ценности."
        )
    },
    {
        "title": "Parasite",
        "title_ru": "Паразиты",
        "year": 2019,
        "description": (
            "Бедная семья постепенно внедряется в жизнь обеспеченных работодателей, "
            "занимая различные должности в их доме. Безобидная афера перерастает "
            "в трагическую историю, обнажающую социальное неравенство."
        )
    }
]


# GET — все фильмы
@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


# GET — один фильм
@lab7.route('/rest-api/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    if film_id < 0 or film_id >= len(films):
        abort(404)
    return jsonify(films[film_id])


# DELETE — удаление фильма
@lab7.route('/rest-api/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    if film_id < 0 or film_id >= len(films):
        abort(404)

    films.pop(film_id)
    return '', 204


# POST — добавление фильма
@lab7.route('/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    new_film = {
        "title": data.get('title', ''),
        "title_ru": data.get('title_ru', ''),
        "year": int(data.get('year', 0)),
        "description": data.get('description', '')
    }

    films.append(new_film)
    return jsonify({"id": len(films) - 1})
