from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify, abort
from random import randint
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                            error = '123123123')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    return redirect('/lab8/login')
    
@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    user = users.query.filter_by(login = login_form).first()
    
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember= False)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')
    
@lab8.route('/lab8/articles/')
@login_required
def articles_list():
    return "Список статей"

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    new_article = articles(title=title, content=content, user_id=current_user.id)
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.user_id != current_user.id:
        abort(403)
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    article.title = request.form.get('title')
    article.content = request.form.get('content')
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.user_id != current_user.id:
        abort(403)
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles/')
