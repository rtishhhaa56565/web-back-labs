from flask import Blueprint, render_template, request, session, jsonify
import json

lab6 = Blueprint('lab6', __name__)

# Данные об офисах
offices = [
    {'number': 1, 'user': None},
    {'number': 2, 'user': None},
    {'number': 3, 'user': None},
    {'number': 4, 'user': None},
    {'number': 5, 'user': None},
    {'number': 6, 'user': None},
    {'number': 7, 'user': None},
    {'number': 8, 'user': None},
    {'number': 9, 'user': None},
    {'number': 10, 'user': None}
]

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32700,
                    'message': 'Parse error'
                }
            })
        
        id = data.get('id', 1)
        method = data.get('method')
        params = data.get('params')
        
        if method == 'info':
            return handle_info(id)
        elif method == 'booking':
            return handle_booking(id, params)
        elif method == 'cancellation':
            return handle_cancellation(id, params)
        else:
            return jsonify({
                'jsonrpc': '2.0',
                'id': id,
                'error': {
                    'code': -32601,
                    'message': 'Method not found'
                }
            })
            
    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'id': data.get('id', 1) if 'data' in locals() else None,
            'error': {
                'code': -32603,
                'message': f'Internal error: {str(e)}'
            }
        })

def handle_info(id):
    """Обработчик метода info - возвращает информацию о пользователе и его арендах"""
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32600,
                'message': 'Неавторизованный пользователь'
            }
        })
    
    # Находим офисы, арендованные текущим пользователем
    user_offices = [office for office in offices if office.get('user') == login]
    office_numbers = [office['number'] for office in user_offices]
    
    return jsonify({
        'jsonrpc': '2.0',
        'id': id,
        'result': {
            'login': login,
            'offices': office_numbers
        }
    })

def handle_booking(id, office_number):
    """Обработчик метода booking - аренда офиса"""
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32600,
                'message': 'Неавторизованный пользователь'
            }
        })
    
    if office_number is None:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32602,
                'message': 'Invalid params'
            }
        })
    
    # Ищем офис
    office_found = False
    for office in offices:
        if office['number'] == office_number:
            office_found = True
            if office.get('user'):
                return jsonify({
                    'jsonrpc': '2.0',
                    'id': id,
                    'error': {
                        'code': -32600,
                        'message': 'Офис уже арендован'
                    }
                })
            # Арендуем офис
            office['user'] = login
            return jsonify({
                'jsonrpc': '2.0',
                'id': id,
                'result': f'Офис №{office_number} успешно арендован'
            })
    
    if not office_found:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32602,
                'message': 'Офис не найден'
            }
        })

def handle_cancellation(id, office_number):
    """Обработчик метода cancellation - снятие аренды офиса"""
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32600,
                'message': 'Неавторизованный пользователь'
            }
        })
    
    if office_number is None:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32602,
                'message': 'Invalid params'
            }
        })
    
    # Ищем офис
    office_found = False
    for office in offices:
        if office['number'] == office_number:
            office_found = True
            
            # Проверяем, арендован ли офис
            if not office.get('user'):
                return jsonify({
                    'jsonrpc': '2.0',
                    'id': id,
                    'error': {
                        'code': -32600,
                        'message': 'Офис не арендован'
                    }
                })
            
            # Проверяем, принадлежит ли аренда текущему пользователю
            if office['user'] != login:
                return jsonify({
                    'jsonrpc': '2.0',
                    'id': id,
                    'error': {
                        'code': -32600,
                        'message': 'Нельзя снять чужую аренду'
                    }
                })
            
            # Снимаем аренду
            office['user'] = None
            return jsonify({
                'jsonrpc': '2.0',
                'id': id,
                'result': f'Аренда офиса №{office_number} успешно отменена'
            })
    
    if not office_found:
        return jsonify({
            'jsonrpc': '2.0',
            'id': id,
            'error': {
                'code': -32602,
                'message': 'Офис не найден'
            }
        })

# Дополнительные маршруты для управления сессией
@lab6.route('/lab6/login/', methods=['POST'])
def login():
    """Маршрут для входа в систему"""
    data = request.get_json()
    login = data.get('login')
    
    if not login:
        return jsonify({'success': False, 'message': 'Логин не может быть пустым'})
    
    session['login'] = login
    return jsonify({'success': True, 'message': f'Вы вошли как {login}'})

@lab6.route('/lab6/logout/', methods=['POST'])
def logout():
    """Маршрут для выхода из системы"""
    session.pop('login', None)
    return jsonify({'success': True, 'message': 'Вы вышли из системы'})

@lab6.route('/lab6/check-auth/')
def check_auth():
    """Маршрут для проверки авторизации"""
    login = session.get('login')
    if login:
        return jsonify({'authenticated': True, 'login': login})
    else:
        return jsonify({'authenticated': False})

@lab6.route('/lab6/offices/')
def get_offices():
    """Маршрут для получения списка всех офисов"""
    return jsonify({'offices': offices})