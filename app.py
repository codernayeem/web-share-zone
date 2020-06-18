import socket, sys
from colorama import init, Fore, Back
from tools import ShareZone

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
app = Flask(__name__, instance_relative_config=False, static_folder='.static', template_folder='.templates')
shareZone = ShareZone()

@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/sharezone')
def share_zone_view():
    global shareZone
    return render_template('share_zone.html', fl_list=shareZone.sharedFiles)

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
