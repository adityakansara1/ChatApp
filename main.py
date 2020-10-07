from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import db
import json
import os


with open('config.json', 'r') as c:
    params = json.load(c)['params']


app = Flask(__name__, template_folder='templets')


app.config['UPLOAD_FOLDER'] = params['db_data']['upload_location']
curr_user_id = 0

@app.route('/', methods=['GET', 'POST'])
def sign_in():
    # if 'username' in session and session['username'] == 'adi':
    #     redirect('index.html')
    # else:
    return render_template('sign-in.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/index', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            passwod = request.form.get('password')
            # session['username'] = username
            
            db.NewUser(username, email, passwod).insertUser()
            return render_template('index.html')
        except Exception as e:
            print(e)

@app.route('/index2', methods=['GET', 'POST'])
def old():
    if request.method == 'POST':
        try:  
            username = request.form.get('username')
            password = request.form.get('password')

            db_obj = db.SignIn(username, password)
            
            if db_obj.checkUser():  
                # session['username'] = 'adi'
                return render_template('index.html')
            else:
                return render_template('sign-in.html')

        except Exception as e:
            print(e)
 

@app.route('/uploadAvatar', methods=['GET', 'POST'])
def uploadAvatar():
    # if 'username' in session and session['username'] == params['username']:
    if True:  
        global curr_user_id
        if request.method == 'POST':
            f = request.files['dp']
            file_extension = os.path.splitext(f.filename)[1]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename('avatar'+str(curr_user_id)+file_extension)))
            db.NewDP(curr_user_id, 'avatar'+str(curr_user_id)+file_extension).insertDp()
            return render_template('index.html')

        

if __name__ == "__main__":
    app.run(debug=True)