from flask import Blueprint, render_template, request, session, jsonify

lab6 = Blueprint('lab6', __name__)

# Генерируем список офисов
offices = []
for i in range(1, 11):
    offices.append({
        'number': i,
        'user': None  # арендатор
    })

@lab6.route('/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        # Получаем информацию о всех офисах
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32600,
                    'message': 'Неавторизованный пользователь'
                },
                'id': id
            }
        
        # Находим офисы, арендованные текущим пользователем
        user_offices = [office for office in offices if office['user'] == login]
        return {
            'jsonrpc': '2.0',
            'result': {
                'login': login,
                'offices': [office['number'] for office in user_offices]
            },
            'id': id
        }
        
    elif data['method'] == 'booking':
        # Бронирование офиса
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32600,
                    'message': 'Неавторизованный пользователь'
                },
                'id': id
            }
        
        office_number = data['params']
        
        # Ищем офис
        for office in offices:
            if office['number'] == office_number:
                if office['user']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32600,
                            'message': 'Офис уже арендован'
                        },
                        'id': id
                    }
                office['user'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'Офис успешно арендован',
                    'id': id
                }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Офис не найден'
            },
            'id': id
        }
        
    elif data['method'] == 'cancellation':
        # Снятие брони офиса
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32600,
                    'message': 'Неавторизованный пользователь'
                },
                'id': id
            }
        
        office_number = data['params']
        
        # Ищем офис
        for office in offices:
            if office['number'] == office_number:
                if not office['user']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32600,
                            'message': 'Офис не арендован'
                        },
                        'id': id
                    }
                
                if office['user'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32600,
                            'message': 'Нельзя снять чужую аренду'
                        },
                        'id': id
                    }
                
                office['user'] = None
                return {
                    'jsonrpc': '2.0',
                    'result': 'Аренда успешно отменена',
                    'id': id
                }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Офис не найден'
            },
            'id': id
        }
    
    else:
        # Метод не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Метод не найден'
            },
            'id': id
        }

# Дополнительные маршруты для управления сессией
@lab6.route('/login/', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    
    if not login:
        return jsonify({'success': False, 'message': 'Логин не может быть пустым'})
    
    session['login'] = login
    return jsonify({'success': True, 'message': f'Вы вошли как {login}'})

@lab6.route('/logout/', methods=['POST'])
def logout():
    session.pop('login', None)
    return jsonify({'success': True, 'message': 'Вы вышли из системы'})

@lab6.route('/check-auth/')
def check_auth():
    login = session.get('login')
    if login:
        return jsonify({'authenticated': True, 'login': login})
    else:
        return jsonify({'authenticated': False})

@lab6.route('/offices/')
def get_offices():
    return jsonify({'offices': offices})