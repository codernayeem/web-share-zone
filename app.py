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

app = Flask(__name__, instance_relative_config=False, static_folder='.static', template_folder='.templates')

db = SQLAlchemy()
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/sharezone')
def share_zone_view():

    return render_template('share_zone.html', fl_list=[])

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
