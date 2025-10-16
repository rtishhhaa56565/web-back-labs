from flask import Blueprint, render_template, request

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)  # Рендерим шаблон вместо пустой строки

@lab3.route('/cookie')
def cookie():
    resp = make_response('установка cookie', 200)
    resp.set_cookie('name','Alex')
    resp.set_cookie('age','20')
    resp.set_cookie('color','magenta')
    return resp