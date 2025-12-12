from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)


@lab7.route('/')
def main():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": (
            "Сотрудник страховой компании, страдающий хронической бессонницей, "
            "встречает харизматичного торговца мылом Тайлера Дёрдена."
        )
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": (
            "Хакер Нео узнаёт, что реальность — иллюзия, созданная машинами."
        )
    },
    {
        "title": "Gladiator",
        "title_ru": "Гладиатор",
        "year": 2000,
        "description": (
            "Римский полководец Максимус становится гладиатором и ищет мести."
        )
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": (
            "Бэтмен противостоит Джокеру, который сеет хаос в Готэме."
        )
    },
    {
        "title": "Parasite",
        "title_ru": "Паразиты",
        "year": 2019,
        "description": (
            "Бедная семья внедряется в дом богатых работодателей."
        )
    }
]


def _validate_id(film_id: int) -> None:
    if film_id < 0 or film_id >= len(films):
        abort(404)


def _parse_year(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/rest-api/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    _validate_id(film_id)
    return jsonify(films[film_id])


@lab7.route('/rest-api/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    _validate_id(film_id)
    films.pop(film_id)
    return '', 204


@lab7.route('/rest-api/films/<int:film_id>', methods=['PUT'])
def edit_film(film_id):
    _validate_id(film_id)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    updated_film = {
        "title": data.get('title', ''),
        "title_ru": data.get('title_ru', ''),
        "year": _parse_year(data.get('year', 0)),
        "description": data.get('description', '')
    }

    films[film_id] = updated_film
    return jsonify(updated_film)


@lab7.route('/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    new_film = {
        "title": data.get('title', ''),
        "title_ru": data.get('title_ru', ''),
        "year": _parse_year(data.get('year', 0)),
        "description": data.get('description', '')
    }

    films.append(new_film)
    return jsonify({"id": len(films) - 1}), 201
