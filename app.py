
from pydoc import describe
from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for, message_flashed

from db import mysql


# models:
from models.ModelUser import ModelUser

# entities:
from models.entities.User import User

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='development'
)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash("invalid password...")
            return render_template('/auth/login.html')
        else:
            flash("user not found")
        return render_template('/auth/login.html')
    else:
        return render_template('/auth/login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        peso = request.form['peso']
        temperatura = request.form['temperatura']
        brix = request.form['brix']
        ph = request.form['ph']
        category = request.form['category']
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO products VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (code, name, stock, value, peso, temperatura, brix, ph, category))
                cur.connection.commit()
                flash('El lote ha sido agregado correctamente', 'success')
            except:
                flash('Un error ha ocurrido o ID del lote repetido', "error")
            return redirect('/home')
    else:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM products ORDER BY code DESC LIMIT 1")
        # cur.execute("SELECT * FROM products")
        data = cur.fetchall()
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
        cur.execute("SELECT * FROM tipo")
        tipo = cur.fetchall()
        print(data)
        return render_template('partials/index.html', data=data, categories=categories, tipo=tipo)


@app.route('/delete/product/<int:code>', methods=['GET', 'POST'])
def delete(code):
    if request.method == 'POST':
        with mysql.cursor() as cur:
            try:
                cur.execute(
                    "DELETE FROM products WHERE code = %s", (code, ))
                cur.connection.commit()
                flash("El producto se ha borrado correctamente", "success")
            except:
                flash(
                    "Ha ocurrido un error mientras intentabamos borrar el producto", "error")
            return redirect('/home')


@app.route('/update/product/<int:code>', methods=['GET', 'POST'])
def update(code):
    if request.method == 'GET':
        with mysql.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE code = %s", (code, ))
            product = cur.fetchone()
        return render_template('partials/update.html', product=product)
    else:
        productCode = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        peso = request.form['peso']
        temperatura = request.form['temperatura']
        brix = request.form['brix']
        ph = request.form['ph']
        category = request.form['category']
        with mysql.cursor() as cur:
            try:
                cur.execute("UPDATE products SET code = %s, name = %s, stock = %s, value = %s, peso = %s, temperatura = %s, brix = %s, ph = %s, id_category = %s WHERE code = %s",
                            (productCode, name, stock, value, peso, temperatura, brix, ph, category, code))
                cur.connection.commit()
                flash("El producto se ha actualizado", "success")
            except:
                flash("Un error ha ocurrido al actualizar el producto", "error")
            return redirect('/home')


@app.route('/create/categorie', methods=['GET', 'POST'])
def create_categorie():
    if request.method == 'POST':
        name = request.form['name']
        cedula = request.form['cedula']
        asociado = request.form['asociado']
        description = request.form['description']
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO categories VALUES(%s, %s, %s, %s)", (name, cedula, asociado, description)) 
                cur.connection.commit()
                flash("La categoria se ha creado", "success")
            except:
                flash("Un error ha ocurrido al crear la categoria", "error")
            return redirect('/home')
    else: 
        return redirect('homes')
    

HOST = 'localhost'
PORT = 4000
DEBUG = True

if(__name__ == '__main__'):
    app.run(HOST, PORT, DEBUG)
