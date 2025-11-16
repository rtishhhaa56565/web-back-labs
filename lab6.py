from flask import Blueprint, render_template, request, session, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

lab6 = Blueprint('lab6', __name__)

# Функция для подключения к PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="web_lab5",  # или ваша база данных
            user="arina_arysheva_knowledge_base",
            password="secure_password_123",
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

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
        
        conn = get_db_connection()
        if not conn:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Ошибка подключения к БД'
                },
                'id': id
            }
        
        try:
            cursor = conn.cursor()
            
            # Находим офисы, арендованные текущим пользователем
            cursor.execute(
                "SELECT number, price FROM offices WHERE user_login = %s",
                (login,)
            )
            user_offices = cursor.fetchall()
            
            user_offices_info = []
            total_cost = 0
            
            for office in user_offices:
                user_offices_info.append({
                    'number': office['number'],
                    'price': office['price']
                })
                total_cost += office['price']
            
            return {
                'jsonrpc': '2.0',
                'result': {
                    'login': login,
                    'offices': user_offices_info,
                    'total_cost': total_cost
                },
                'id': id
            }
            
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': f'Ошибка БД: {str(e)}'
                },
                'id': id
            }
        finally:
            cursor.close()
            conn.close()
        
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
        
        conn = get_db_connection()
        if not conn:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Ошибка подключения к БД'
                },
                'id': id
            }
        
        try:
            cursor = conn.cursor()
            
            # Проверяем, свободен ли офис
            cursor.execute(
                "SELECT user_login, price FROM offices WHERE number = %s",
                (office_number,)
            )
            office = cursor.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32602,
                        'message': 'Офис не найден'
                    },
                    'id': id
                }
            
            if office['user_login']:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32600,
                        'message': 'Офис уже арендован'
                    },
                    'id': id
                }
            
            # Арендуем офис
            cursor.execute(
                "UPDATE offices SET user_login = %s WHERE number = %s",
                (login, office_number)
            )
            conn.commit()
            
            return {
                'jsonrpc': '2.0',
                'result': f'Офис №{office_number} успешно арендован за {office["price"]} руб./мес.',
                'id': id
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': f'Ошибка БД: {str(e)}'
                },
                'id': id
            }
        finally:
            cursor.close()
            conn.close()
        
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
        
        conn = get_db_connection()
        if not conn:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Ошибка подключения к БД'
                },
                'id': id
            }
        
        try:
            cursor = conn.cursor()
            
            # Проверяем офис
            cursor.execute(
                "SELECT user_login FROM offices WHERE number = %s",
                (office_number,)
            )
            office = cursor.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32602,
                        'message': 'Офис не найден'
                    },
                    'id': id
                }
            
            if not office['user_login']:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32600,
                        'message': 'Офис не арендован'
                    },
                    'id': id
                }
            
            if office['user_login'] != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32600,
                        'message': 'Нельзя снять чужую аренду'
                    },
                    'id': id
                }
            
            # Снимаем аренду
            cursor.execute(
                "UPDATE offices SET user_login = NULL WHERE number = %s",
                (office_number,)
            )
            conn.commit()
            
            return {
                'jsonrpc': '2.0',
                'result': f'Аренда офиса №{office_number} успешно отменена',
                'id': id
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': f'Ошибка БД: {str(e)}'
                },
                'id': id
            }
        finally:
            cursor.close()
            conn.close()
    
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
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Ошибка подключения к БД'})
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT number, user_login as user, price FROM offices ORDER BY number")
        offices = cursor.fetchall()
        return jsonify({'offices': offices})
    except Exception as e:
        return jsonify({'error': f'Ошибка БД: {str(e)}'})
    finally:
        cursor.close()
        conn.close()