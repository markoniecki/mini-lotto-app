from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import mapa_plot, wykres_plot, db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_fallback_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    mapa_plot.create_heatmap('static/chart_data/mapa.png')
    return render_template('mapa.html')

@app.route('/wykres')
def wykres_menu():
    return render_template('wykres_menu.html')

@app.route('/wykres/static')
def wykres_static():
    wykres_plot.generate_trend_plot()
    return render_template('wykres_static.html')

@app.route('/wykres/dynamic')
def wykres_dynamic():
    script, div = wykres_plot.generate_trend_plot_bokeh()
    return render_template('wykres_dynamic.html', script=script, div=div)

@app.route('/art', methods=['GET', 'POST'])
def art():
    if request.method == 'POST':
        if 'user' not in session:
            flash("Zaloguj się, aby dodać propozycję.")
            return redirect(url_for('login'))

        text = request.form['fragment']
        db.add_art_proposal(session['user'], text)
        flash("Dziękujemy za propozycję!")
        return redirect(url_for('art'))

    proposals = db.get_all_proposals()
    return render_template('art.html', proposals=proposals)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        if 'user' not in session:
            flash("Zaloguj się, aby dodać post.")
            return redirect(url_for('login'))

        title = request.form['title']
        content = request.form['content']
        db.add_forum_post(session['user'], title, content)
        flash("Dodano post.")
        return redirect(url_for('forum'))

    posts = db.get_all_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if db.validate_login(user, pwd):
            session['user'] = user
            flash("Zalogowano pomyślnie.")
            return redirect(url_for('art'))
        flash("Błąd logowania.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if db.create_user(user, pwd):
            flash("Rejestracja udana. Możesz się zalogować.")
            return redirect(url_for('login'))
        flash("Użytkownik już istnieje.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Wylogowano.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
