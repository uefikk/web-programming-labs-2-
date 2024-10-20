from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

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

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Contrnt-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Ефимова Юлия Алексеевна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename = "oak.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <link rel = "stylesheet" href="''' + style +'''"
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''" class="oak-image">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('reset_counter')
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br>
        <a href="''' + reset_link + '''">Очистить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

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

@app.route('/lab1')
def lab1():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>Лабораторная 1</title>
        </head>
           <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/">Главная страница</a></li>
                    <li><a href="/index">Главная страница (index)</a></li>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab1/web">Web</a></li>
                    <li><a href="/lab1/author">Автор</a></li>
                    <li><a href="/lab1/oak">Дуб</a></li>
                    <li><a href="/lab1/counter">Счетчик</a></li>
                    <li><a href="/lab1/info">Информация</a></li>
                    <li><a href="/lab1/created">Создано успешно</a></li>
                    <li><a href="/error/400">Ошибка 400</a></li>
                    <li><a href="/error/401">Ошибка 401</a></li>
                    <li><a href="/error/402">Ошибка 402</a></li>
                    <li><a href="/error/403">Ошибка 403</a></li>
                    <li><a href="/error/405">Ошибка 405</a></li>
                    <li><a href="/error/418">Ошибка 418</a></li>
                    <li><a href="/trigger_error">Триггер ошибки</a></li>
                    <li><a href="/ecstra">Битва экстрасенсов)</a></li>
                </ul>
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

@app.route('/ecstra')
def ecstra():
    path = url_for("static", filename = "ecstra.jpg")
    style = url_for("static", filename = "lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + style +'''"
        <title>Вся правда о «Битве экстрасенсов»</title>
        <style>
            body {
                background-color: black;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>ЧЕРЕДА ТРАГЕДИЙ</h1>
        <p>
            Юлия бежала от страшных воспоминаний в Москву, хотя с родным городом до конца не рассталась – здесь у нее была квартира, друзья, сюда хотелось когда-нибудь вернуться.
            И как только выдалась возможность, сибирячка подала заявку на участие в 10 сезоне «Битвы экстрасенсов». Говорит, реально верила в способности магов, борющихся за победу в самом рейтинговом шоу страны. 
            Хотела проверить, смогут ли они «увидеть» ее беды и рассказать их причины. Интересовал Юлию и главный вопрос: сможет ли она еще родить ребенка? Ведь на тот момент женщине было уже 36 лет.
        </p>
        <p>
            Итак, съемки. Первое испытание для людей с паранормальными способностями стало довольно сложным: нужно было рассказать, что связывает четырех героинь в студии. 
            Экстрасенсы терялись, кто-то говорил, что дамы многодетны, кто-то, наоборот, говорил, что они сделали аборты. Не запуталась лишь главная звезда того сезона, Джулия Ванг.
        </p>
        <p>
            - Тебе надо переехать в другой город, если ты хочешь детей! - сказала Джулия, всматриваясь в глаза Юлии. - Рядом с тобой старая больница. Ты потеряла всех родных, остался один муж.
        </p>
        <p>
            - Это было правдой, - рассказывает Юлия. – Она угадала не только про родных. Муж у меня действительно на тот момент был. Про больницу тоже совпало. В Иркутске я жила в микрорайоне Юбилейный, 
            недалеко от морга. И Джулия советовала быстрее «сваливать» и тогда ребенок точно родится. Кстати, что касается переезда, то на тот момент я как раз уехала с супругом в Москву, мне оставалось лишь продать все имущество в Иркутске.
        </p>
        <img src="''' + path + '''" alt="ecstra">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru',
    'X-Custom-Header-1': 'ecstra',
    'X-Custom-Header-2': 'OMG'
}

if __name__ == '__main__':
    app.run(debug=True)

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

