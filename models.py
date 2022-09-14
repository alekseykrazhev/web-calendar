from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager


database = SQLAlchemy()
login = LoginManager()


class EventInfo(database.Model):
    __tablename__ = 'events'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    event = database.Column(database.String(100), nullable=False)
    date = database.Column(database.Date, nullable=False)


class UserModel(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(80), unique=True)
    username = database.Column(database.String(100))
    password_hash = database.Column(database.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
