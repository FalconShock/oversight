import os, sys
from flask import Flask, render_template, request, redirect, session, g, url_for
from flaskext.mysql import MySQL
#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = os.urandom(24)

global person_name
person_name = ''
global person_occupation
person_occupation = ''

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'vulcan'
app.config['MYSQL_DATABASE_DB'] = 'secretariat'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.4'
app.config['MYSQL_DATABASE_PORT'] = 6603
mysql.init_app(app)

@app.route('/')
def go_to_login(): return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session: g.user = session['user']

@app.route('/login')
def login(): return render_template('login.html')

@app.route('/verification', methods = ['POST','GET'])
def verify():

    if request.method == 'POST':
        session.pop('user', None)
        person_email = request.form['loginUsername']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT password from secretariat.masters WHERE username="%s"' % person_email)
        data = cursor.fetchall()

        if request.form['loginPassword'] == data[0][0]:

            session['user'] = person_email
            cursor.execute('SELECT name from secretariat.masters WHERE username="%s"' % person_email)
            g.name = cursor.fetchall()[0][0]
            cursor.execute('SELECT occupation from secretariat.masters WHERE username="%s"' % person_email)
            g.occupation = cursor.fetchall()[0][0]
            return render_template('index.html', name = g.name, occ = g.occupation)

    else: return redirect(url_for('login'))

@app.route('/dashboard')
def index():

    if g.user: return render_template('index.html', name = g.name, occ = g.occupation)
    return redirect(url_for('login'))

@app.route('/projects', methods = ['POST','GET'])
def projects():

    if g.user:
    	conn = mysql.connect()
    	cursor = conn.cursor()

    	if request.method == "POST":
    		field_name = request.form['field']
    		if field_name == "Futuristic Computer Sciences": field = "cse"
    		elif field_name == "Next-Generation Electronics": field = "ece"
    		elif field_name == "Polity & Global Governance": field = "pgg"
    		elif field_name == "Artificial & Augmented Intelligence": field = "aai"

    		cursor.execute("SELECT project_id, name, mentee, domain, requirement,\
    		proposal from projects.%s WHERE status='Unclaimed'" % field)
    		data = cursor.fetchall()
    		cursor.execute("select * from information_schema.COLUMNS\
    		where TABLE_NAME='%s'" % field)
    		data_columns = cursor.fetchall()
    		data_columns = [x[3] for x in data_columns[:-3]]

    	else:
    		data = ["None"]
    		data_columns = ["None"]
    	    #conn.close()

    	return render_template('projects.html', data = data, col = data_columns)

    else: redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

"""
	<!DOCTYPE HTML>
	<p>%s</p>
	"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, host='0.0.0.0', port=port)
