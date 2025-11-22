from flask import Blueprint, render_template, request, session, current_app
from models import db, Office

lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def main():
    login = session.get('login')

    # Вычисляем общую стоимость арендованных пользователем офисов из БД    
    total_cost = 0
    if login:
        user_offices = Office.query.filter_by(tenant=login).all()
        total_cost = sum(office.price for office in user_offices)
    
    return render_template('lab6/lab6.html', 
                         login=login, 
                         total_cost=total_cost)


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        # Получаем все офисы из базы данных
        try:
            offices = Office.query.order_by(Office.number).all()
            offices_list = [office.to_dict() for office in offices]
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            current_app.logger.error(f"Ошибка при получении офисов: {e}")
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Internal server error'
                },
                'id': id
            }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        
        try:
            office = Office.query.filter_by(number=office_number).first()
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id    
                }
            
            if office.tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id   
                }
            
            office.tenant = login
            db.session.commit()
            
            return {
                'jsonrpc': '2.0',
                'result': "success",  
                'id': id
            }
            
        except Exception as e:
            current_app.logger.error(f"Ошибка при бронировании: {e}")
            db.session.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Internal error'
                },
                'id': id
            }

    if data['method'] == 'cancellation':
        office_number = data['params']
        
        try:
            office = Office.query.filter_by(number=office_number).first()
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id    
                }
            
            if not office.tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office is not booked'
                    },
                    'id': id    
                }
            
            if office.tenant != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'You are not the tenant of this office'
                    },
                    'id': id    
                }
            
            office.tenant = None
            db.session.commit()
            
            return {
                'jsonrpc': '2.0',
                'result': "success",  
                'id': id
            }
            
        except Exception as e:
            current_app.logger.error(f"Ошибка при снятии аренды: {e}")
            db.session.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': 'Internal error'
                },
                'id': id
            }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }