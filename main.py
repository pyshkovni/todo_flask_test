# ###################################################################
# ############## СОЗДАНИЕ САЙТА С ПОМОЩЬЮ PYTHON-FLASK ##############
# ###################################################################

# ЗАДАЧА:
# - написать веб-приложение Заметочника

# Официальная документация фрейворка flask
# https://flask.palletsprojects.com/en/2.2.x/

# Официальная документация клиента для работы с БД - Flask-SQLAlchemy
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/

# скачать пакет flask-sqlalchemy через оболочку
# pip install flask-sqlalchemy

# тест гит!!!!

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# создаем экземпляр класса объекта Flask, то есть наше приложение
# создаем экземпляр класса объекта базы данных SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    todo_lst = Todo.query.all()  # запрос всех заметок из базы банных
    return render_template('index.html', todo_lst=todo_lst) 


@app.route("/add", methods=["POST"])
def add():
    title = request.form['content']  # принимаем заметку из формы с сайта
    new_todo = Todo(title=title, complete=False)  # создаем экземпляр заметки
    db.session.add(new_todo)  # открываем сессию с базой данных
    db.session.commit()  # подтверждаем изменения в базе данных
    return redirect(url_for('index'))  # возвращаемя обратно на страницу


@app.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # фильруем заметки по идентификатору
    db.session.delete(todo)  # удаляем заметку
    db.session.commit()  # подтверждаем изменения в базе данных
    return redirect(url_for("index"))  # возвращаемя обратно на страницу


@app.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # фильруем заметки по идентификатору
    todo.complete = not todo.complete  # делаем инверию значения True/False
    db.session.commit()  # подтверждаем изменения в базе данных
    return redirect(url_for("index"))  # возвращаемя обратно на страницу

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)

