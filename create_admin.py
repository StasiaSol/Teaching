from getpass import getpass
import sys
from webapp import create_app 
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    user_name = input('Введите имя:')
    if User.query.filter(User.user_name == user_name).count():
        print('Такой пользователь уже есть.')
        sys.exit(0)

    password1 = getpass('Введите пароль:')
    password2 = getpass('Повторите пароль:')
    if not password1 == password2:
        print('Пароли не совпадают.')
        sys.exit(0)

    new_user = User(user_name = user_name, role = 'admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id {}'.format(new_user.id))
    