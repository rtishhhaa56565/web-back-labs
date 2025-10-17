from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/')
def lab():
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)

@lab3.route('/cookie')
def cookie():
    resp = make_response('установка cookie')
    resp.set_cookie('name', 'Alex')
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')
    return resp

@lab3.route('/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('color', '', expires=0)
    return resp