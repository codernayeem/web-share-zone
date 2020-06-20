from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from colorama import init, Fore, Back
from datetime import datetime
import socket, sys, config as cfg

init()
host = socket.gethostbyname(socket.gethostname())
port = 1999
if len(sys.argv) == 2:
    host = sys.argv[1]
elif len(sys.argv) == 3:
    if sys.argv[1] != '*':
        host = sys.argv[1]
    port = int(sys.argv[2])
elif len(sys.argv) > 3:
    print('\n[+] - Too Many Parameters')
    exit(1)

print(f'\n\t ****  WEB SHARE ZONE ****\n')
print(' * Host : ', host)
print(' * Port : ', port)


app = Flask(__name__, instance_relative_config=False, static_folder='.static', template_folder='.templates')

db = SQLAlchemy()
app.config.from_object('config.Config')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'flask-users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    is_admin = db.Column(db.Boolean, index=False, nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    created_on = db.Column(db.DateTime, index=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, nullable=True)

    def get_name(self):
        if not self.fullname:
            return self.fullname
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


def save_db(data):
    db.session.add(data)
    db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        redirect('/')
    if request.method == 'GET':
        error = session.get('error_login')
        if error:
            session['error_login'] = None
        return render_template('login.html', error=error)
    
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        if user.check_password(request.form['password']):
            remember = False
            if request.form.get('remember', None) == 'on':
                remember = True
            login_user(user, remember=remember)
            user.last_login = datetime.now()
            save_db(user)
            return redirect('/')
        session['error_login'] = 'Incorrect username or password'
    else:
        session['error_login'] = 'User not Found'
    return redirect('/login')


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/sharezone')
def share_zone_view():

    return render_template('share_zone.html', fl_list=[])

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
