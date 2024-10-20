from flask import Flask, url_for, redirect, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename = "404.png")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
<head>
    <link rel = "stylesheet" href="''' + style +'''"
</head>
    <body>
        <img src="''' + path + '''" class="full-screen-image">
    </body>
</html>
''', 404

@app.route('/')
@app.route('/index')
def index():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
           <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
           </header>
           <body>
                <a href='/lab1'>Первая лабораторная</a>
           </body>
           <footer>Ефимова Юлия Алексеевна, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/error/400')
def error_400():
    return 'Bad Request', 400

@app.route('/error/401')
def error_401():
    return 'Unauthorized', 401

@app.route('/error/402')
def error_402():
    return 'Payment Required', 402

@app.route('/error/403')
def error_403():
    return 'Forbidden', 403

@app.route('/error/405')
def error_405():
    return 'Method Not Allowed', 405

@app.route('/error/418')
def error_418():
    return "I'm a teapot", 418

@app.route('/trigger_error')
def trigger_error():
    # Вызываем ошибку деления на ноль
    return 1 / 0

@app.errorhandler(500)
def internal_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>Произошла ошибка на сервере</h1>
        <p>Пожалуйста, попробуйте позже.</p>
    </body>
</html>
''', 500

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'
    
flower_list =  ['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flower/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
        <html>
        <head>
            <title>Цветок</title>
        </head>
        <body>
            <h1>Цветок: {flower_name}</h1>
            <a href="/lab2/flowers">Посмотреть все цветы</a>
        </body>
        </html>
        '''

@app.route('/lab2/add_flower/')
def flower_f():
    return 'Вы не задали имя цветка', 400

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name in flower_list:
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Такой цветок уже есть, попробуй другой</h1>
            <p>Список цветков: {flower_list} </p>
            </body>
        </html>'''
    else: 
        flower_list.append(name)
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name} </p>
            <p>Список цветков: {flower_list} </p>
            </body>
        </html>'''

@app.route('/lab2/flowers')
def all_flowers():
    return f'''
    <p>Список цветков: {','.join(flower_list)}</p>
    <p>Количество цветов: {len(flower_list)}</p>
    '''


@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    return '''
    <html>
    <head>
        <title>Список цветов очищен</title>
    </head>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
    </html>
    '''

@app.route('/lab2/example')
def example():
    name = 'Ефимова Юлия'
    group = 'фби-72'
    course = 9 
    lab_num = 100
    fruits = [
        {'name': 'яблоки', 'price' : 100},
        {'name': 'груши', 'price' : 120},
        {'name': 'апельсины', 'price' : 80},
        {'name': 'мандарины', 'price' : 95},
        {'name': 'манго', 'price' : 321}
        ]
    return render_template('example.html', lab_num=lab_num, fruits=fruits)

@app.route('/lab2/')
def lab2():
    links = [
    {"url": "/lab2/example", "text": "example"},
    {"url": "/lab2/a", "text": "/lab2/a"},
    {"url": "/lab2/a/", "text": "/lab2/a/"},
    {"url": "/lab2/flower/1", "text": "Кол-во цветов"},
    {"url": "/lab2/filters", "text": "Фильтры"},
    {"url": "/lab2/add_flower/rose", "text": "Добавить цветок"},
    {"url": "/lab2/add_flower/", "text": "Забыл написать цветок"},
    {"url": "/lab2/flowers", "text": "Список цветов и кол-во"},
    {"url": "/lab2/clear_flowers", "text": "Очистка списка цветов"},
    {"url": '/lab2/calc/14/28', "text": "Калькулятор"},
    {"url": '/lab2/calc/1', "text": "Перенаправление"}
]
    return render_template('lab2.html', links=links)

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..'
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>') 
def calc(a, b): 
    result_1 = a + b 
    result_2 = a - b 
    result_3 = a * b 
    result_4 = a / b 
    result_5 = a ** b 
    return ''' 
    <html> 
    <head> 
        <title>Расчёт с параметрами</title> 
    </head> 
    <body> 
        <h1>Расчёт с параметрами</h1> 
        <p>{a} + {b} = {result_1}</p> 
        <p>{a} - {b} = {result_2}</p> 
        <p>{a} * {b} = {result_3}</p> 
        <p>{a} / {b} = {result_4}</p> 
        <p>{a} ^ {b} = {result_5}</p> 
    </body> 
    </html> 
    '''.format(a=a, b=b, result_2=result_2, result_1=result_1,
result_3=result_3, result_4=result_4, result_5=result_5) 
 
@app.route('/lab2/calc/<int:a>') 
def redirect_to_default(a): 
    return redirect(f'/lab2/calc/{a}/1') 

