'''
chores, the website
'''

__version__ = '0.0.0'

import copy
import datetime
import os
import platform
import uuid

from dateutil.relativedelta import relativedelta
import flask
import flask_sqlalchemy
import sqlalchemy as sa
import sqlalchemy_utils as sau


here = os.path.dirname(os.path.realpath(__file__))

app = flask.Flask('chores')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{here}/data/chores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


class Chore(db.Model):
    __tablename__ = 'chores'

    assignees = [
        ('0', 'Alex'),
        ('1', 'Marissa'),
    ]

    cadences = [
        ('0', 'Weekly'),
        ('1', 'Monthly'),
        ('2', 'Every Two Weeks'),
        ('3', 'Every Two Months'),
        ('4', 'Every Three Months'),
    ]

    id = sa.Column(sau.UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sa.Column(sa.String(80), nullable=False)
    assignee = sa.Column(sau.ChoiceType(assignees), nullable=False)
    cadence = sa.Column(sau.ChoiceType(cadences), nullable=False)
    next_due_date = sa.Column(sa.Date, nullable=False)

    @staticmethod
    def validate_missing(data):
        required = ['name', 'assignee', 'cadence', 'next_due_date']
        return [f for f in required if not data.get(f)]

    @staticmethod
    def validate_values(data):
        invalid, clean = [], {}

        name = data.get('name', '')
        if len(name) > 80:
            invalid.append('name is greater than 80 chars')
        else:
            clean['name'] = name

        try:
            assignee = str(int(data.get('assignee')))
            valid_assignees = [a[0] for a in Chore.assignees]
            if assignee not in valid_assignees:
                invalid.append(f'assignee not one of {valid_assignees}')
            else:
                clean['assignee'] = assignee
        except (TypeError, ValueError):
            invalid.append('assignee is not an integer')

        try:
            cadence = str(int(data.get('cadence')))
            valid_cadences = [a[0] for a in Chore.cadences]
            if cadence not in valid_cadences:
                invalid.append(f'cadence not one of {valid_cadences}')
            else:
                clean['cadence'] = cadence
        except (TypeError, ValueError):
            invalid.append('cadence is not an integer')

        try:
            clean['next_due_date'] = datetime.datetime.strptime(
                data.get('next_due_date', ''), '%Y-%m-%d'
            )
        except ValueError:
            invalid.append('next_due_date is not in %Y-%m-%d format')

        return invalid, clean

    @staticmethod
    def validate(data):
        missing = Chore.validate_missing(data)
        invalid, clean = Chore.validate_values(data)
        return missing, invalid, clean

    def toJsonSafe(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'assignee': str(self.assignee.code),
            'cadence': str(self.cadence.code),
            'next_due_date': str(self.next_due_date),
        }

    @property
    def next_due_delta(self):
        cadence = int(self.cadence.code)

        if cadence == 0:
            return relativedelta(days=7)
        elif cadence == 1:
            return relativedelta(months=+1)
        elif cadence == 2:
            return relativedelta(days=+14)
        elif cadence == 3:
            return relativedelta(months=+2)
        elif cadence == 4:
            return relativedelta(months=+3)
        else:
            raise ValueError(f'unexpected cadence type {self.cadence}')

    def find_next_due_date(self):
        today = datetime.datetime.now().date()
        next_due = copy.copy(self.next_due_date)

        if next_due > today:  # eager beaver, advance into future
            return next_due + self.next_due_delta
        else:  # slacker, keep advancing until caught up
            while not (next_due > today):
                next_due += self.next_due_delta

            return next_due


@app.route('/', methods=['GET'])
def index():
    return flask.render_template(
        'index.html',
        globals={
            'assignees': dict(Chore.assignees),
            'cadences': dict(Chore.cadences),
            'api_url': f'{flask.request.url}api/',
        }
    )


@app.route('/api/status/', methods=['GET'])
def status():
    return {
        'python': platform.python_version(),
        'timestamp': datetime.datetime.now().timestamp(),
        'version': __version__,
    }


@app.route('/api/chores/', methods=['GET', 'POST'])
def chores_list():
    if flask.request.method == 'GET':
        chores = Chore.query.all()
        return flask.jsonify([c.toJsonSafe() for c in chores])

    data = flask.request.get_json(force=True)

    missing, invalid, clean = Chore.validate(data)
    if missing or invalid:
        app.logger.debug('could not create chore from data = %s', data)
        return flask.jsonify(missing=missing, invalid=invalid), 400

    app.logger.debug('creating new chore from data = %s', clean)
    chore = Chore(**clean)
    db.session.add(chore)
    db.session.commit()
    return flask.jsonify(chore.toJsonSafe()), 201


@app.route('/api/chores/<uuid:id>/', methods=['GET', 'DELETE', 'PUT'])
def chores_detail(id):
    app.logger.debug('fetching chore with id %s', id)
    chore = Chore.query.get_or_404(id)

    if flask.request.method == 'GET':
        return flask.jsonify(chore.toJsonSafe()), 200

    if flask.request.method == 'DELETE':
        app.logger.debug('deleting chore with id %s', id)
        db.session.delete(chore)
        db.session.commit()
        return '', 204

    if flask.request.method == 'PUT':
        data = flask.request.get_json(force=True)

        missing, invalid, clean = Chore.validate(data)

        if missing or invalid:
            app.logger.debug('could not update chore from data = %s', data)
            return flask.jsonify(missing=missing, invalid=invalid), 400

        app.logger.debug('updating new chore from data = %s', clean)
        chore.name = clean['name']
        chore.assignee = clean['assignee']
        chore.cadence = clean['cadence']
        chore.next_due_date = clean['next_due_date']
        db.session.commit()
        db.session.refresh(chore)
        return flask.jsonify(chore.toJsonSafe()), 201


@app.route('/api/chores/<uuid:id>/complete/', methods=['POST'])
def chores_complete(id):
    app.logger.debug('fetching chore with id %s', id)
    chore = Chore.query.get_or_404(id)
    chore.next_due_date = chore.find_next_due_date()
    db.session.add(chore)
    db.session.commit()
    db.session.refresh(chore)
    return flask.jsonify(chore.toJsonSafe()), 200


if __name__ == '__main__':
    app.run(debug=True)
