from flask import Flask, Blueprint, render_template, redirect, request, session, Response, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils  import secure_filename
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from colorama import init, Fore, Back
from datetime import datetime
import socket, sys, config as cfg

from tools import Path, join, create_folder, get_formatted_datetime, get_downloadzone_files, encode64, decode64, sizeSince, is_valid_file, get_icon

init()
app = Flask(__name__, instance_relative_config=False, static_folder='.static', template_folder='.templates')

db = SQLAlchemy()
app.config.from_object('config.Config')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def inject_common_data():
    return dict(encode64=encode64, decode64=decode64, sizeSince=sizeSince, get_icon=get_icon)


class User(UserMixin, db.Model):
    __tablename__ = 'flask-users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    is_admin = db.Column(db.Boolean, index=False, nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    created_on = db.Column(db.DateTime, index=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, nullable=True)

    def get_name(self):
        if self.fullname:
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


admin_bp = Blueprint('admin_bp', __name__)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self, name, **kwargs):
        return Response(status=403)

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self, name, **kwargs):
        return Response(status=403)

admin = Admin(app, name='Web Share Zone', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
app.register_blueprint(admin_bp)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(request.args.get('next') or '/')
    if request.method == 'GET':
        error = session.get('error_login')
        info = session.get('login_info')
        if error:
            session['error_login'] = None
        if info:
            session['login_info'] = None
        return render_template('login.html', error=error, info=info)
    
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        if user.check_password(request.form['password']):
            remember = False
            if request.form.get('remember', None) == 'on':
                remember = True
            login_user(user, remember=remember)
            user.last_login = datetime.now()
            save_db(user)
            return redirect(request.args.get('next') or '/')
        session['error_login'] = 'Incorrect username or password'
    else:
        session['error_login'] = 'User not Found'
    return redirect('/login')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        error = session.get('signup_error')
        if error:
            session['signup_error'] = None
        if not cfg.CAN_SIGNUP:
            return render_template('signup.html', error = 'Signup system is currently not avaiable')
        return render_template('signup.html', error=error)

    if not cfg.CAN_SIGNUP:
        return redirect(url_for('signup_page'))

    email = request.form.get('email')
    username = request.form.get('username')
    fullname = request.form.get('fullname')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        session['signup_error'] = 'The username is already used'
    elif not (username and password):
        session['signup_error'] = 'Please, provide all information'
    else:
        new_user = User(is_admin=False, email=email, fullname=fullname, username=username)
        new_user.set_password(password)
        new_user.created_on = datetime.now()
        save_db(new_user)

        session['login_info'] = 'Signup Successfull'
        return redirect(url_for('login_page'))
        
    return redirect(url_for('signup_page'))


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/sharezone')
def share_zone_view():

    return render_template('share_zone.html', fl_list=[])


@app.route('/downloadzone')
def downloadzone_view():
    if not current_user.is_authenticated:
        return redirect(url_for('login_page', next='/downloadzone'))
    
    files, total_size, sort, order = get_downloadzone_files(cfg.DOWNLOAD_ZONE_PATH)
    return render_template('download_zone.html', fl_list=files, total_count=len(files), total_size=total_size)


@app.route('/downloadzone/download')
def downloadzone_download():
    if not current_user.is_authenticated:
        return Response(status=403)
    fl = request.args.get('fl')

    if fl and is_valid_file(join(cfg.DOWNLOAD_ZONE_PATH, fl)):
        return send_from_directory(cfg.DOWNLOAD_ZONE_PATH, fl, as_attachment=True)

    return Response(status=404)


@app.route('/uploadzone')
def uploadzone_view():
    if not current_user.is_authenticated:
        return redirect(url_for('login_page', next='/uploadzone'))
    
    error = session.get('uploadzone_error')
    info = session.get('uploadzone_info')
    if error:
        session['uploadzone_error'] = None
    if info:
        session['uploadzone_info'] = None

    return render_template('upload_zone.html', error=error, info=info, max_limit=cfg.MAX_CONTENT_LENGTH_IN_MB)


@app.route('/uploadzone', methods=['POST'])
def uploadzone_upload():
    if not current_user.is_authenticated:
        return redirect(url_for('login_page', next=url_for('uploadzone_view')))

    fl = request.files.get('file')
    if fl and fl.filename:
        filename = secure_filename(fl.filename)
        p = join(cfg.UPLOAD_ZONE_PATH, get_formatted_datetime('%d-%m-%Y %H-%M-%S'))
        if not Path(p).exists():
            create_folder(p)
        fl.save(join(p, filename))
        session['uploadzone_info'] = 'Uploaded Successfully'
        return redirect(url_for('uploadzone_view'))

    else:
        session['uploadzone_error'] = 'Upload Failed. File not found'
        return redirect(url_for('uploadzone_view'))


if __name__ == "__main__":
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
    app.run(host=host, port=port, debug=True)
