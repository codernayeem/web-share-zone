# instructions
# python manage.py init          |   Create database
# python manage.py createadmin   |   Create Admin Account
# python manage.py createuser    |   Create Normal User Account

import sys
from app import db, app, User
from getpass import getpass
from datetime import datetime

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        with app.app_context() as app_cntxt:
            db.create_all()
        print('[+] - Database created')

    elif sys.argv[1] == 'createadmin' or sys.argv[1] == 'createuser':
        if sys.argv[1] == 'createadmin':
            print('[+] - Creating Admin ...')
        else:
            print('[+] - Creating a new User ...')
            
        username = input('Username : ')
        print('[+] - Password will be hidden when you type.')
        password = getpass('Password : ')
        password_ = getpass('Confirm Password : ')
        if password != password_:
            print('[+] - Password not matched')
            exit(0)
        if username and password:
            with app.app_context() as app_cntxt:
                user = User.query.filter_by(username=username).first()
                if user:
                    print('[+] - Username already used')
                else:
                    user = User()
                    user.username = username
                    user.set_password(password)
                    if sys.argv[1] == 'createadmin':
                        user.is_admin = True
                    else:
                        user.is_admin = False
                    user.created_on = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    print('[+] - User created => ', username)
        else:
            print('[+] - Invalid User or password')

    else:
        print('[+] - Please, give valid a command')
else:
    print('''
[+] - Please, give a command from below :
  ==> Create database :
    - python manage.py init
  ==> Create Admin Account :
    - python manage.py createadmin
  ==> Create Normal User Account :
    - python manage.py createuser''')
