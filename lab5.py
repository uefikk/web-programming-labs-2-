from flask import Flask, Blueprint, render_template, request, make_response, redirect, session, url_for, current_app
import traceback
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/index.html', login = session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':    
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'db1',
            user = 'db1',
            password = '123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)

    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        error_message = 'Заполните все поля!'
        return render_template('lab5/login.html', error=error_message)

    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, password FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT login, password FROM users WHERE login = ?;", (login,))
            
        
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль не верны')
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль не верны')

        db_close(conn, cur)

        # Устанавливаем логин пользователя в сессию
        session['login'] = login

        return render_template('lab5/success_login.html', login=login)

    except psycopg2.Error as e:
        # Логирование ошибки
        print(f"Ошибка при работе с базой данных: {e}")
        return render_template('lab5/login.html', error='Ошибка при входе. Попробуйте позже.')



@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка наличия логина и пароля
    if not login or not password:
        error_message = 'Заполните все поля!'
        if not login:
            error_message = 'Логин не может быть пустым!'
        elif not password:
            error_message = 'Пароль не может быть пустым!'
        return render_template('lab5/register.html', error=error_message)

    try:
        conn, cur = db_connect()
        
        # Проверка на существование пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s;", (login,)) 
        else:
            cur.execute("SELECT login FROM users WHERE login = ?;", (login,)) 
        
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        password_hash = generate_password_hash(password)
        # Добавление нового пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        else:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        db_close(conn, cur)

        return render_template('lab5/success.html', login=login)

    except Exception as e:
        # Предоставляем сообщение об ошибке пользователю
        return render_template('lab5/register.html', error='Ошибка регистрации: ' + str(e))


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = 'is_public' in request.form
    is_favorite = 'is_favorite' in request.form

    # Проверка на заполнение всех полей
    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля!')

    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user_id = cur.fetchone()['id']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public, is_favorite)
                VALUES (%s, %s, %s, %s, %s);
            """, (user_id, title, article_text, is_public, is_favorite))
        else:
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public, is_favorite)
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, title, article_text, is_public, is_favorite))

        conn.commit()
        db_close(conn, cur)

        return redirect(url_for('lab5.lab'))

    except Exception as e:
        print(f"Ошибка при создании статьи: {e}")
        traceback.print_exc()
        return render_template('lab5/create_article.html', error='Ошибка при создании статьи: ' + str(e))


@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user_id = cur.fetchone()['id']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = %s 
                ORDER BY is_favorite DESC, id ASC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = ? 
                ORDER BY is_favorite DESC, id ASC;
            """, (user_id,))
        
        articles = cur.fetchall()
        db_close(conn, cur)

        return render_template('lab5/list.html', articles=articles)

    except Exception as e:
        print(f"Ошибка при получении статей: {e}")
        return render_template('lab5/list.html', error='Ошибка при получении статей: ' + str(e))


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id = ?;", (article_id,))
        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return render_template('lab5/list.html', error='Статья не найдена')

        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = 'is_public' in request.form
    is_favorite = 'is_favorite' in request.form

    if not title or not article_text:
        return render_template('lab5/edit_article.html', error='Заполните все поля!')

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE articles 
                SET title = %s, article_text = %s, is_public = %s, is_favorite = %s 
                WHERE id = %s;
            """, (title, article_text, is_public, is_favorite, article_id))
        else:
            cur.execute("""
                UPDATE articles 
                SET title = ?, article_text = ?, is_public = ?, is_favorite = ? 
                WHERE id = ?;
            """, (title, article_text, is_public, is_favorite, article_id))
        conn.commit()
        db_close(conn, cur)
        return redirect(url_for('lab5.list_articles'))
    except Exception as e:
        print(f"Ошибка при редактировании статьи: {e}")
        return render_template('lab5/edit_article.html', error='Ошибка при редактировании статьи: ' + str(e))


@lab5.route('/lab5/delete/<int:article_id>', methods=['GET'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id = %s;", (article_id,))
        else:
            cur.execute("DELETE FROM articles WHERE id = ?;", (article_id,))
        conn.commit()
        db_close(conn, cur)
        return redirect(url_for('lab5.list_articles'))
    except Exception as e:
        print(f"Ошибка при удалении статьи: {e}")
        return render_template('lab5/list.html', error='Ошибка при удалении статьи: ' + str(e))

@lab5.route('/lab5/users', methods=['GET'])
def list_users():
    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users;")
        else:
            cur.execute("SELECT login FROM users;")
        
        users = cur.fetchall()
        db_close(conn, cur)

        return render_template('lab5/users.html', users=users)

    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return render_template('lab5/users.html', error='Ошибка при получении пользователей: ' + str(e))


@lab5.route('/lab5/public_articles', methods=['GET'])
def public_articles():
    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE is_public = TRUE ORDER BY id ASC;")
        else:
            cur.execute("SELECT * FROM articles WHERE is_public = TRUE ORDER BY id ASC;")
        
        articles = cur.fetchall()
        db_close(conn, cur)

        return render_template('lab5/public_articles.html', articles=articles)

    except Exception as e:
        print(f"Ошибка при получении публичных статей: {e}")
        return render_template('lab5/public_articles.html', error='Ошибка при получении публичных статей: ' + str(e))