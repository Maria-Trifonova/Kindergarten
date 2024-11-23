from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '12345abcd'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'kindergarten'
mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def glav_html():
    return render_template('test.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM parents WHERE login = %s and password = %s" , (username, password))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session['username'] = username
            flash('Вы успешно авторизовались', 'success')
            return render_template('dashboard.html')
        else:
            flash('Пароль или логин неверен', 'danger')

    return render_template('login.html')

@app.route('/registr', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO parents(login, password) VALUES(%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Вы успешно зарегестрировались', 'success')
        return redirect(url_for('login'))

    return render_template('registr.html')

if __name__ == '__main__':
    app.run(debug=True)