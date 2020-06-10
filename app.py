'''
chores, the website
'''

__version__ = '0.0.0'

import datetime
import json
import os
import platform
import uuid

import flask
import flask_sqlalchemy
import sqlalchemy as sa
import sqlalchemy_utils as sau


here = os.path.dirname(os.path.realpath(__file__))

app = flask.Flask('chores')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{here}/data/chores.db'
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
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    assignee = sa.Column(sau.ChoiceType(assignees), nullable=False)
    cadence = sa.Column(sau.ChoiceType(cadences), nullable=False)
    next_due_date = sa.Column(sa.Date, nullable=False)

    @staticmethod
    def validate(data):
        required = ['name', 'assignee', 'cadence', 'next_due_date']
        missing = [f for f in required if not data.get(f)]

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
                data.get('next_due_date', ''), '%d-%m-%Y'
            )
        except ValueError:
            invalid.append('next_due_date is not in %d-%m-%Y format')

        return missing, invalid, clean

    def toJsonSafe(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'assignee': str(self.assignee.code),
            'cadence': str(self.cadence.code),
            'next_due_date': str(self.next_due_date),
        }


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


if __name__ == '__main__':
    app.run(debug=True)
