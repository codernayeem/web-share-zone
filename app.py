import socket, sys, config as cfg
from colorama import init, Fore, Back

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


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
app = Flask(__name__, instance_relative_config=False, static_folder='.static', template_folder='.templates')

db = SQLAlchemy()
app.config.from_object('config.Config')
db.init_app(app)


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


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/sharezone')
def share_zone_view():

    return render_template('share_zone.html', fl_list=[])

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
