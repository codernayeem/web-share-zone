import sys
from app import db, app

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        with app.app_context() as app_cntxt:
            db.create_all()
        print('[+] - Database created')
    else:
        print('[+] - Please, give valid a command')
else:
    print('[+] - Please, give a command')
