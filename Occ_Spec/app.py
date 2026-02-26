from flask import *
import sqlite3 

def create_db():
    conn = sqlite3.connect("/workspaces/College_Projects/Occ_Spec/account_database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                UserFullName TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Points INTEGER DEFAULT 0
        ); 
    """)

    conn.commit()
    conn.close()

def validate_pass(password):
    SpecialSym = ['$', '@', '#', '%', '!']
    val = True
    length = len(password)

    if length < 8:
        val = False
        
    if length > 20:
        val = False

    # Check for digits
    if not any(char.isdigit() for char in password):
        val = False

    # Check for uppercase letters
    if not any(char.isupper() for char in password):
        val = False

    # Check for lowercase letters
    if not any(char.islower() for char in password):
        val = False

    # Check for special symbols
    if not any(char in SpecialSym for char in password):
        val = False

    return val


app = Flask(__name__)

app.secret_key = "9f8c4e2a1b7d9a5f3c8e6d2b4a1f0c9e5d7b2a4c6f8e1d3c5b7a9f2e4d6c8b0"

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = sqlite3.connect("/workspaces/College_Projects/Occ_Spec/account_database.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE username = ? AND email = ? AND password = ?", (username, email, password))
            result = cur.fetchone()

            conn.close()

            if result:
                session['username'] = result[1]
                session['fullName'] = result[2]
                session['points'] = result[5]
                return redirect(url_for('home'))
            else:
                return render_template("login.html", alert_message="Account not found. Please try again")
            
        except:
            return render_template("login.html", alert_message="Database error. Please try again")

        
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
            return render_template("register.html", alert_message="Passwords do not match. Please try again.")
            
        else:
            if validate_pass(password) == False:
                return render_template("register.html", alert_message="Password must be between 8 and 20 characters, have at least one upper case and lowercase character and include one of the following $, @, #, %, !.")
            else:
                try:
                    conn = sqlite3.connect("/workspaces/College_Projects/Occ_Spec/account_database.db")
                    cur = conn.cursor()

                    cur.execute("""
                        INSERT INTO users (Username, UserFullName, Email, Password)
                        VALUES (?, ?, ?, ?)
                    """, (username, fullName, email, password))

                    conn.commit()
                    conn.close()

                    return render_template("register.html", alert_message="Account registered successfully. Please login")
                
                
                except:
                    return render_template("register.html", alert_message="Details entered have already been used. Please try again")

    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def forgotPass():
    return render_template('login.html', alert_message="Contact support@gibjohn.com or your IT admin to reset your password.")

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
    fullName = session.get('fullName')
    points = session.get('points')
    current_user = session.get('username')

    conn = sqlite3.connect("/workspaces/College_Projects/Occ_Spec/account_database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT Username, Points 
        FROM users 
        ORDER BY Points DESC
        LIMIT 10
    """)

    users = cur.fetchall()
    conn.close()

    return render_template('profile.html', fullName=fullName, points=points, users=users, current_user=current_user)

@app.route('/videos', methods = ['GET', 'POST'])
def videos():
    return render_template('subject_selector.html')

@app.route('/mathsVideos', methods = ['GET', 'POST'])
def maths_vids():
    return render_template('videos.html')

@app.route('/englishVideos', methods = ['GET', 'POST'])
def english_vids():
    return render_template('videos.html')

@app.route('/scienceVideos', methods = ['GET', 'POST'])
def science_vids():
    return render_template('videos.html')

@app.route('/historyVideos', methods = ['GET', 'POST'])
def history_vids():
    return render_template('videos.html')

@app.route('/geographyVideos', methods = ['GET', 'POST'])
def geography_vids():
    return render_template('videos.html')

@app.route('/musicVideos', methods = ['GET', 'POST'])
def music_vids():
    return render_template('videos.html')

@app.route('/reasources', methods = ['GET', 'POST'])
def resources():
    return render_template('resources.html')

@app.route('/quizzes', methods = ['GET', 'POST'])
def quizzes():
    return render_template('resources.html')

@app.route('/readingMaterial', methods = ['GET', 'POST'])
def reading_material():
    return render_template('resources.html')

@app.route('/notes', methods = ['GET', 'POST'])
def notes():
    return render_template('resources.html')

@app.route('/worksheets', methods = ['GET', 'POST'])
def worksheets():
    return render_template('resources.html')

@app.route('/flashcards', methods = ['GET', 'POST'])
def flashcards():
    return render_template('resources.html')

@app.route('/presentations', methods = ['GET', 'POST'])
def presentations():
    return render_template('resources.html')

@app.route('/games', methods = ['GET', 'POST'])
def games():
    return render_template('games.html')

@app.route('/crosswords', methods = ['GET', 'POST'])
def crosswords():
    return render_template('games.html')

@app.route('/hangman', methods = ['GET', 'POST'])
def hangman():
    return render_template('games.html')

@app.route('/bingo', methods = ['GET', 'POST'])
def bingo():
    return render_template('games.html')

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    create_db()
    app.run()