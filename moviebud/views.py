from models import User
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app._static_folder = "/home/pratik/Downloads/MovieBud/moviebud/static"

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/register', methods=['GET','POST'])    
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['password2']

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif (password != repassword):
        	flash('Passwords do not match')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['login'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
	
        if not User(username).verify_password(password):
            flash('Invalid username/password')
        else:
            session['login'] = username
            return redirect(url_for('home'))

    return render_template('login.html')
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
    	you = session.get('login')
    	you = User(you).get_name()
    	return render_template('home.html', you=you)
    	 
@app.route('/mutualfriends', methods=['GET', 'POST'])
def mutualfriends():
    if request.method == 'GET':
    	log = session.get('login')
    	mutual = User(log).get_mutual_friends()

    	return render_template('mutual.html', result=mutual)
    	
@app.route('/moviepref', methods=['GET', 'POST'])
def moviepref():
    if request.method == 'GET':
    	log = session.get('login')
    	recommendation = User(log).movie_pref()

    	return render_template('moviepref.html', result=recommendation)

@app.route('/discover', methods=['GET', 'POST'])
def discover():
	return render_template('discovermovies.html')
   
@app.route('/addfriend/<friendtoadd>')
def addfriend(friendtoadd):
	user_adding = session.get('login');
	response = User(user_adding).add_friend(friendtoadd)
	
	name = User(friendtoadd).get_name()
	
	message = str(name[0][0]) + " added!"
	
	return render_template('home.html', message=message)
	
@app.route('/friendsmovies')
def friendsmovies():
	you = session.get('login');
	response = User(you).friend_recommendation()
	
	return render_template('friendsmovies.html', rec = response)
	
@app.route('/genremovies')
def genremovies():
	you = session.get('login');
	response = User(you).genre_recommendation()
	
	return render_template('genremovies.html', rec = response, genre = response[0][1])
	
@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		you = session.get('login');
		title = request.form['title']
		response = User(you).moviedetails(title)
		
		if response:
			return render_template('moviepage.html', rec=response, title=title)
		else:
			flash("Movie Not Present in DataBase")
			return render_template('searchmovie.html')
	
	if request.method == 'GET':
		return render_template('searchmovie.html')

@app.route('/ratemovie/<title>', methods=['GET', 'POST'])
def ratemovie(title):
	if request.method == 'POST':
		rating = request.form['rating']
		rating = int(rating)
		if rating<1 or rating>5:
			flash("Rating must be between 1-5")
			you = session.get('login')
			response2 = User(you).moviedetails(title)
			return render_template('moviepage.html', rec=response2, title=title)
	
		else:
			you = session.get('login')
			response = User(you).rate(title, rating)
			response2 = User(you).moviedetails(title)
			flash("Rated Succesfully")
			return render_template('moviepage.html', rec=response2, title=title)
