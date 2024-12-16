from flask import Blueprint, render_template, abort, request
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "The Age of Adaline",
        "title_ru": "Век Адалин",
        "year": 2015,
        "description": "Адалин Боуман — столетняя молодая женщина 1908 года рождения. После автокатастрофы и поражения молнией в 1937 году \
        она перестала стареть. Каждые десять лет она меняет личность, документы, работу и окружение. Неизменными спутниками для неё остаются только стареющая дочь,\
        подруга — слепая пианистка, не знающая возраста Адалин, и десятая по счёту собака одной и той же породы. Однажды на праздновании Нового года Адалин встречает\
        симпатичного молодого человека по имени Эллис, ради которого ей хочется перестать убегать."
    },
    {
        "title": "Now You See Me",
        "title_ru": "Иллюзия обмана",
        "year": 2013,
        "description": "Команда лучших иллюзионистов мира проворачивает дерзкие ограбления прямо во время своих шоу, играя в кошки-мышки с агентами ФБР."
    },
    {
        "title": "Paddington",
        "title_ru": "Приключения Паддингтона",
        "year": 2014,
        "description": "Познакомьтесь, это медведь по имени Паддингтон из дремучего Перу. Он приехал в Лондон, чтобы обрести семью и стать настоящим \
        английским джентльменом. На пути к этой цели его ожидают невероятные приключения, полные юмора и опасностей."
    },
    {
        "title": "Mothers' Instinct",
        "title_ru": "Материнский инстинкт",
        "year": 2024,
        "description": "Начало 1960-х, американский пригород. Элис и Селин — лучшие подруги. Они живут в соседних домах, их сыновья учатся в одном классе и растут как братья, \
        а знаменательные даты две семьи отмечают вместе. Но этой идиллии приходит конец после несчастного случая. Дружба женщин трещит по швам и оборачивается взаимными подозрениями и упрёками."
    },
    {
        "title": "The Intern",
        "title_ru": "Стажёр",
        "year": 2015,
        "description": "70-летний вдовец Бен Уитакер обнаруживает, что выход на пенсию — еще не конец. Пользуясь случаем, он становится старшим стажером в интернет-магазине модной одежды под руководством Джулс Остин."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id >= len(films):
        return abort(404)
    else:
        return films[id]
    
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id >= len(films):
        return abort(404)
    else:
        del films[id]
        return '', 204
    
@lab7.route('lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id >= len(films):
        return abort(404)
    else:
        film = request.get_json()
        films[id] = film
        return films[id]