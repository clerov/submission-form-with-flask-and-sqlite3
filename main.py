from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def create_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (fullname TEXT, age INTEGER, email TEXT, contact TEXT)")
    connection.commit()
    connection.close()


def insert_form_data(name, age, email, contact):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
                   (name, age, email, contact))
    connection.commit()
    connection.close()


def view_values():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    connection.close()
    print(rows)
    return rows


@app.route('/')
def home():
    create_table()
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    form = request.form
    try:
        insert_form_data(form['name'], form['age'],
                         form['email'], form['contact'])
        return render_template('success.html')
    except TypeError as error:
        return render_template('error.html')


@app.route('/users')
def users():
    return view_values()


if __name__ == "__main__":
    app.run(debug=True)
