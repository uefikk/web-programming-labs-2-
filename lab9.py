from flask import Blueprint, render_template, request, redirect, session

lab9 = Blueprint('lab9', __name__)

# Секретный ключ для работы с сессиями
lab9.secret_key = 'your_secret_key'

# Главная страница с формой для ввода имени
@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        session['sender_name'] = request.form.get('sender_name')
        return redirect('/lab9/age')  
    return render_template('/lab9/index.html')

# Страница для ввода возраста
@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect('/lab9/gender')  
    return render_template('/lab9/age.html')

# Страница для выбора пола
@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect('/lab9/preference')  
    return render_template('/lab9/gender.html')

# Страница для выбора предпочтений
@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        session['preference'] = request.form.get('preference')
        return redirect('/lab9/sweet')  
    return render_template('/lab9/preference.html')

# Страница для выбора сладкого или сытного
@lab9.route('/lab9/sweet', methods=['GET', 'POST'])
def sweet_or_savory():
    if request.method == 'POST':
        session['sweet'] = request.form.get('sweet')
        return redirect('/lab9/card')  
    return render_template('/lab9/sweet.html')

# Страница с поздравлением
@lab9.route('/lab9/card', methods=['GET'])
def card():
    sender_name = session.get('sender_name')
    age = session.get('age')
    gender = session.get('gender')
    preference = session.get('preference')
    sweet = session.get('sweet')

    # Логика для генерации поздравления
    if gender == 'male':
        congrats = f"Поздравляю тебя, {sender_name}! Желаю, чтобы ты быстро вырос, был умным и счастливым!"
    else:
        congrats = f"Поздравляю тебя, {sender_name}! Желаю, чтобы ты быстро выросла, была умной и счастливой!"

    # Логика для выбора картинки
    if sweet == 'sweet':
        image = 'candy.jpg'
    else:
        image = 'cake.jpg'

    return render_template('/lab9/card.html', congrats=congrats, image=image)

