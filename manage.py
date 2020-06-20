import sys
from app import db, app, User
from getpass import getpass

if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        with app.app_context() as app_cntxt:
            db.create_all()
        print('[+] - Database created')
    if sys.argv[1] == 'createadmin':
        print('[+] - Creating Admin ...')
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
                    user.is_admin = True
                    db.session.add(user)
                    db.session.commit()
                    print('[+] - User created => ', username)
        else:
            print('[+] - Invalid User or password')

    else:
        print('[+] - Please, give valid a command')
else:
    print('[+] - Please, give a command')
