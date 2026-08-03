from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, initialize_database
from config import SECRET_KEY
import sqlite3, re

app = Flask(__name__)
app.secret_key = SECRET_KEY
initialize_database()

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        fullname=request.form["fullname"].strip()
        email=request.form["email"].strip()
        age=request.form["age"].strip()
        if not fullname: flash("Full name is required"); return redirect(url_for("register"))
        if not is_valid_email(email): flash("Invalid email"); return redirect(url_for("register"))
        try: age=int(age)
        except: flash("Age must be numeric"); return redirect(url_for("register"))
        try:
            conn=get_db_connection()
            conn.execute("INSERT INTO users(fullname,email,age) VALUES(?,?,?)",(fullname,email,age))
            conn.commit(); conn.close()
            flash("User registered successfully")
        except sqlite3.IntegrityError:
            flash("Email already exists")
        return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/users")
def users():
    conn=get_db_connection(); users=conn.execute("SELECT * FROM users").fetchall(); conn.close()
    return render_template("users.html", users=users)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    conn=get_db_connection(); user=conn.execute('SELECT * FROM users WHERE id=?',(user_id,)).fetchone(); conn.close()
    if user is None: return 'User not found',404
    return render_template('profile.html', user=user)

@app.route('/update/<int:user_id>', methods=['GET','POST'])
def update(user_id):
    conn=get_db_connection(); user=conn.execute('SELECT * FROM users WHERE id=?',(user_id,)).fetchone()
    if request.method=='POST':
        conn.execute('UPDATE users SET fullname=?,email=?,age=? WHERE id=?',(request.form['fullname'],request.form['email'],request.form['age'],user_id))
        conn.commit(); conn.close()
        return redirect(url_for('profile', user_id=user_id))
    conn.close()
    return render_template('update.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)