import os, sys
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')

app = Flask(__name__)
app.static_folder = "static"

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'vulcan'
#app.config['MYSQL_DATABASE_DB'] = 'mysql'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.6'
mysql.init_app(app)

@app.route('/')
def go_to_login(): return redirect('/login')

@app.route('/login')
def login(): return render_template('login.html')

@app.route('/verification', methods = ['POST','GET','PUT'])
def verify():
    email = request.form['loginUsername']
    password = request.form['loginPassword']
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT authentication_string from mysql.user WHERE user = %s" % email)
    data = cursor.fetchall()

    if password == data:
        return redirect('/dashboard')
    else: return redirect('/login')

@app.route('/dashboard')
def index(): return render_template('index.html')

@app.route('/projects')
def projects(): 
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT id, name, password from secretariat.masters")
	data = cursor.fetchall()
	cursor.execute("select * from information_schema.COLUMNS\
	where TABLE_NAME='masters'")
	data_columns = cursor.fetchall()
	#conn.close()
	return render_template('projects.html', data = data, col = data_columns)

"""
@app.route('/uploader', methods = ['POST','GET','PUT'])
def upload_file():
    f = request.files['file']
    result = summarize(f.read(), ratio=0.5)
    out_file = open('temp.txt', 'w+')
    out_file.write(result)
    out_file_addr = os.path.
    return render_template('output.html', result = result,\
    out_file_addr = out_file_addr)
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7777))
    app.run(debug = True, host='0.0.0.0', port=port)
