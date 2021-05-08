from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import json
import random, datetime, time

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tukangsapu0721'
app.config['MYSQL_DB'] = 'db_tugasakhir'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("welcome.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/admin',methods=["GET","POST"])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM tb_admin WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['admin'] = user['name']
                session['email'] = user['email']
                return render_template("welcome.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
        
    else:
        return render_template("admin.html")

@app.route('/registeradmin', methods=["GET", "POST"])
def registeradmin():
    if request.method == 'GET':
        return render_template("registeradmin.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        otp = request.form['otp']
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        if otp == 'rehan123':
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tb_admin (name, email, password) VALUES (%s,%s,%s)",(name,email,hashed,))
            mysql.connection.commit()
            session['admin'] = name
            session['email'] = email
            return redirect(url_for('welcome'))
        else:
            return render_template("otpwrong.html")

@app.route('/user',methods=["GET","POST"])
def user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM tb_user WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['user'] = user['name']
                session['email'] = user['email']
                return render_template("welcome.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
        
    else:
        return render_template("user.html")

@app.route('/registeruser', methods=["GET", "POST"])
def registeruser():
    if request.method == 'GET':
        return render_template("registeruser.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_user (name, email, password) VALUES (%s,%s,%s)",(name,email,hashed,))
        mysql.connection.commit()
        session['user'] = name
        session['email'] = email
        return redirect(url_for('welcome'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("welcome.html")

#HVACWeb
@app.route('/databaseadmin',methods= ["POST","GET"])
def databaseadmin():
    return render_template("databaseadmin.html")

@app.route('/databaseuser',methods= ["GET"])
def databaseuser():
    return render_template("databaseuser.html")

@app.route('/database',methods= ["POST","GET"])
def database():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_hvac")
    rvhvac = cur.fetchall()
    return jsonify(rvhvac=rvhvac)

@app.route('/hapus-databaseadmin', methods=["GET"])
def hapusdatabaseadmin():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_hvac")
    mysql.connection.commit()
    return ('', 204)
#EndService

#HVACApp
@app.route('/apphvac')
def apphvac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_hvac")
    #row_headers=[x[0] for x in cur.description] 
    rv = cur.fetchall()
    cur.close()
    return render_template('apphvac.html', apphvac=rv)

@app.route('/hvacdelete', methods=["POST", "GET"])
def hvacdelete():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tb_hvac")
        mysql.connection.commit()
    return redirect(url_for('apphvac'))
#EndApp

if __name__ == '__main__':
    app.secret_key = "rehan123"
    app.run(host='0.0.0.0', debug=True)