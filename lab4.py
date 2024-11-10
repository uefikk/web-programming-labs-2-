from flask import Blueprint, render_template, request, make_response, redirect, session
import traceback
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():

    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    try:
        x1 = int(x1)
        x2 = int(x2)
        
        if x2 == 0:
            return render_template('lab4/div.html', error='Деление на ноль невозможно!')
        
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/div.html', error='Пожалуйста, введите корректные числа!')
    
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', 0)
    x2 = request.form.get('x2', 0)
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 + x2
        return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/sum.html', error='Пожалуйста, введите корректные числа!')


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', 1)
    x2 = request.form.get('x2', 1)
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 * x2
        return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/mul.html', error='Пожалуйста, введите корректные числа!')


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/sub.html', error='Пожалуйста, введите корректные числа!')


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        
        if x1 == 0 and x2 == 0:
            return render_template('lab4/pow.html', error='Недопустимые значения!')
        
        result = x1 ** x2
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/pow.html', error='Пожалуйста, введите корректные числа!')

tree_count = 0


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123'},
    {'login': 'bob', 'password': '555'},
    {'login': 'alik', 'password': '666'},
    {'login': 'egor', 'password': '777'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
        else:
            authorized = False
            login = ''
        return render_template("lab4/login.html", authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error = error, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/refrigerator', methods=['GET', 'POST'])
def refrigerator():
    result = None
    
    if request.method == 'POST':
        temperature = request.form.get('temperature')

        # Проверьте, что temperature всегда строка, и обработайте это
        if temperature:
            try:
                temperature = float(temperature)  # Преобразование, возможно, вызовет ошибку
            except ValueError:
                return render_template('lab4/refrigerator.html', result='Ошибка: введено некорректное значение температуры')

            # Здесь ваши проверки
            if temperature < -12:
                result = 'Не удалось установить температуру — слишком низкое значение'
            elif temperature > -1:
                result = 'Не удалось установить температуру — слишком высокое значение'
            elif -12 <= temperature < -9:
                result = f'Установлена температура: {temperature}°C ❄️❄️❄️'
            elif -8 <= temperature < -5:
                result = f'Установлена температура: {temperature}°C ❄️❄️'
            elif -4 <= temperature < -1:
                result = f'Установлена температура: {temperature}°C ❄️'
        else:
            result = 'Ошибка: не задана температура'

    return render_template('lab4/refrigerator.html', result=result)