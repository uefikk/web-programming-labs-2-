from flask import Flask, Blueprint, render_template, request, jsonify, session  
 
lab6 = Blueprint('lab6', __name__)  
 
offices = []  
for i in range(1, 11):  
    offices.append({"number": i, "tenant": ""})  
 
@lab6.route('/lab6/')  
def main():  
    return render_template('lab6/lab6.html')  
 
 
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])  
def api():  
    data = request.json  
    id = data['id']  
    if data['method'] == 'info':  
        return jsonify({  
            'jsonrpc': '2.0',  
            'result': offices,  
            'id': id  
        }) 
         
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
        for office in offices: 
            if office['number'] == office_number: 
                if office ['tenant'] !='': 
                    return { 
                        'jsonrpc': '2.0', 
                        'error': { 
                            'code': 2, 
                            'message': 'Unauthorized' 
                    }, 
                    'id': id 
                    } 
                     
                office['tenant'] = login 
                return { 
                    'jsonrpc': '2.0', 
                    'result': 'success', 
                    'id': id 
                }