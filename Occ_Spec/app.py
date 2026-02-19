from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3 

def create_db():
    conn = sqlite3.connect("account_database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                UserFullName TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL
        ); 
    """)

    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = sqlite3.connect("account_database.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE username = ? AND email = ? AND password = ?", (username, email, password))
            result = cur.fetchone()

            conn.close()

            if result:
                return redirect(url_for('home'))
            else:
                return "Your login credentials are incorrect"
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

        
    return render_template('login.html')
    
@app.route('/register', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        fullName = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        confirmPass = request.form['confirmPass']

        if password != confirmPass:
            return "Your passwords dont match"

        else:
            try:
                conn = sqlite3.connect("account_database.db")
                cur = conn.cursor()

                cur.execute("""
                    INSERT INTO users (Username, UserFullName, Email, Password)
                    VALUES (?, ?, ?, ?)
                """, (username, fullName, email, password))

                conn.commit()
                conn.close()

                return "You account has been registered"
            except:
               return redirect(url_for('register_error'))

    return render_template('register.html')

@app.route('/forgotPass', methods = ['GET', 'POST'])
def forgotPass():
    return render_template('forgotPass.html')

@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login_error', methods = ['GET', 'POST'])
def login_error():
    return render_template('login_error.html')

@app.route('/register_error', methods = ['GET', 'POST'])
def register_error():
    return render_template('register_error.html')

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/videos', methods = ['GET', 'POST'])
def videos():
    return render_template('videos.html')

@app.route('/reasources', methods = ['GET', 'POST'])
def resources():
    return render_template('resources.html')

@app.route('/games', methods = ['GET', 'POST'])
def games():
    return render_template('games.html')

if __name__ == '__main__':
    create_db()
    app.run()