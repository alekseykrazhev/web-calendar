import secrets
from datetime import datetime

from flask import Flask, request, abort, render_template, redirect
from flask_cors import CORS
from flask_login import login_required, current_user, login_user, logout_user
from flask_restful import reqparse, inputs

from models import EventInfo, database, UserModel, login

app = Flask(__name__)
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

parser = reqparse.RequestParser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)
login.init_app(app)
CORS(app)

parser.add_argument("event",
                    type=str,
                    help="The event name is required!",
                    required=True)
parser.add_argument("date",
                    type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)
'''
Authentication block

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

database = SQLAlchemy(app)
login = LoginManager(app)


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



end block
'''


@app.route('/')
@login_required
def main_page():
    return render_template('main.html'), 200


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event_page():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        event = request.form.get('event')
        date = request.form.get('date')
        ei = EventInfo()
        ei.event = event
        ei.date = datetime.strptime(date, '%Y-%m-%d')
        database.session.add(ei)
        database.session.commit()

    args = request.args
    start_time = args.get('start_time')
    end_time = args.get('end_time')

    if start_time and end_time:
        events = EventInfo.query.filter(EventInfo.date >= start_time, EventInfo.date <= end_time).all()
    else:
        events = EventInfo.query.all()
    ans = []

    for event in events:
        ans.append({'id': event.id, 'event': event.event, 'date': event.date.strftime('%Y-%m-%d')})

    return render_template('event.html', events=ans), 200


@app.route('/event/today')
@login_required
def today_event():
    today = datetime.now().date()
    events = EventInfo.query.filter_by(date=today).all()
    ans = []

    if events:
        for event in events:
            ans.append({'id': event.id, 'event': event.event, 'date': event.date.strftime('%Y-%m-%d')})
        # return ans

    return render_template('today.html', events=ans), 200


@app.route('/event/<int:event_id>', methods=['GET', 'DELETE'])
@login_required
def event_by_id(event_id):
    if request.method == 'GET':
        event = EventInfo.query.filter(EventInfo.id == event_id).first()

        if event is None:
            abort(404, "The event doesn't exist!")

        return render_template('event_by_id.html', event=event), 200

    elif request.method == 'DELETE':
        event = EventInfo.query.filter(EventInfo.id == event_id).first()

        if event is None:
            abort(404, "Error 404: The event doesn't exist!")

        database.session.delete(event)
        database.session.commit()

        return 'The event has been deleted!', 200


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)

            return redirect('/')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return 'Email is already in use'

        user = UserModel(email=email, username=username)
        user.set_password(password)
        database.session.add(user)
        database.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
