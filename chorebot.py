import datetime
import json
import os
import time
import sys

import requests

USERS = {
    '0': '@alex',
    '1': '@marissa'
}


class Chore(object):
    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return f'<Chore "{self.name}">'

    @property
    def name(self):
        return self.response['name']

    @property
    def next_due(self):
        return datetime.datetime.strptime(self.response['next_due_date'], '%Y-%m-%d').date()

    @property
    def due_today(self):
        return self.next_due == datetime.datetime.today().date()

    @property
    def overdue(self):
        return self.next_due < datetime.datetime.today().date()

    @property
    def assignee(self):
        return USERS[str(self.response['assignee'])]


def log(msg, *args):
    print('chorebot: {}'.format(msg.format(*args)))


def format_chore_list(chores):
    return '\n'.join(['- ' + chore.name for chore in chores])


def main():
    log('starting chorebot')

    hub_url = os.environ.get('HUB_URL', 'http://hub.local')
    log('using Hub URL {}', hub_url)

    chores = [Chore(d) for d in requests.get(f'{hub_url}/api/chores/').json()]
    log('fetched {} chores', len(chores))

    webhook = os.environ['WEBHOOK_URL']
    log('using secret webhook url')

    for user in USERS.values():
        mine = list(filter(lambda c: c.assignee == user, chores))
        log('collected {} chores for {}', len(mine), user)
        today = list(filter(lambda c: c.due_today, mine))
        log('found {} chores for {} due today', len(today), user)
        overdue = list(filter(lambda c: c.overdue, mine))
        log('found {} chores for {} overdue', len(overdue), user)

        if not any([today, overdue]):
            log('no chores due today or overdue for {}, skipping', user)
            continue

        message = 'Greetings!\n'

        if today:
            message += f'''
The following chores are due today:
{format_chore_list(today)}
            '''

        if overdue:
            message += f'''
The following chores are overdue:
{format_chore_list(overdue)}
            '''

        message += '''
Have a wonderful day.'''

        log('sending slack reminder to {}', user)
        response = requests.post(
            webhook,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'text': message,
                'channel': user,
                'username': 'reckerbot',
                'icon_emoji': ':reckerbot:'
            })
        )
        response.raise_for_status()


if __name__ == '__main__':
    main()
