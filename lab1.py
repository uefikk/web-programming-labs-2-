from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/oak')
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

@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@lab1.route("/lab1/info")
def info():
    return redirect("/author")


@lab1.route("/lab1/created")
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


@lab1.route('/lab1')
def lab():
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
                    <li><a href="/lab1/ecstra">Битва экстрасенсов)</a></li>
                </ul>
           </body>
           <footer>Ефимова Юлия Алексеевна, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200


@lab1.route('/lab1/ecstra')
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
    lab1.run(debug=True)