from datetime import datetime
from flask import Flask, request, abort, render_template
from flask_cors import CORS
from flask_restful import reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
parser = reqparse.RequestParser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

parser.add_argument("event",
                    type=str,
                    help="The event name is required!",
                    required=True)
parser.add_argument("date",
                    type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)


class EventInfo(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)


@app.route('/')
def main_page():

    return render_template('main.html'), 200


@app.route('/event', methods=['GET', 'POST'])
def event_page():

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        event = request.form.get('event')
        date = request.form.get('date')
        ei = EventInfo()
        ei.event = event
        ei.date = datetime.strptime(date, '%Y-%m-%d')
        db.session.add(ei)
        db.session.commit()

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
def event_by_id(event_id):

    if request.method == 'GET':
        event = EventInfo.query.filter(EventInfo.id == event_id).first()

        if event is None:
            abort(404, "The event doesn't exist!")

        return render_template('event_by_id.html', event=event), 200

    elif request.method == 'DELETE':
        event = EventInfo.query.filter(EventInfo.id == event_id).first()

        if event is None:
            abort(404, "The event doesn't exist!")

        db.session.delete(event)
        db.session.commit()

        return 'The event has been deleted!', 200


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
