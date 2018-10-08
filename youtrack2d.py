import threading

import httplib2
import os
import requests
import re
from youtrackAPI.python.youtrack import connection

from Issues import Issues


class Youtrack2csv:
    def __init__(self):
        self.login = '***********'
        self.password = '***********'
        self.connection = None
        self.issues = Issues()

    def get_issues(self):
        yt = connection.Connection("https://outer-heaven.myjetbrains.com/youtrack", self.login, self.password)
        self.connection = yt
        print('Projects : ', yt.getProjectIds())
        print('Number of issues: ', yt.getNumberOfIssues())
        print('Getting issues...')
        for y in (yt.getIssues(projectId='PEI', filter='', after=0, max=100)):
            try:
                if 'resolved' in y.__dict__ and 'Spent time' in y.__dict__ and 'description' in y.__dict__:
                    self.issues.add_issue(priority=y.__getitem__('Priority'), id=y.__getitem__('id'),
                                          stage=y.__getitem__('Stage'), spent_time=y.__getitem__('Spent time'),
                                          description=y.__getitem__('description') + '&nbsp;<br> (For more '
                                                                                     'information go to: '
                                                                                     'https://outer-heaven'
                                                                                     '.myjetbrains.com/youtrack'
                                                                                     '/issue/' + y.__getitem__(
                                              'id') + ')',
                                          resolved=y.__getitem__('resolved'),
                                          estimation=y.__getitem__('Estimation'), created=y.__getitem__('created'),
                                          assignee=y.__getitem__('Assignee'), summary=y.__getitem__('summary'),
                                          assignee_team=y.__getitem__('Assignee Team'),
                                          sprint=y.__getitem__('sprint')
                                          )
                if 'Spent time' in y.__dict__:
                    self.issues.add_issue(priority=y.__getitem__('Priority'), id=y.__getitem__('id'),
                                          stage=y.__getitem__('Stage'), spent_time=y.__getitem__('Spent time'),
                                          description=y.__getitem__('description') + '&nbsp;<br> (For more '
                                                                                     'information go to: '
                                                                                     'https://outer-heaven'
                                                                                     '.myjetbrains.com/youtrack'
                                                                                     '/issue/' + y.__getitem__('id')
                                                      + ')',
                                          resolved='',
                                          estimation=y.__getitem__('Estimation'), created=y.__getitem__('created'),
                                          assignee=y.__getitem__('Assignee'), summary=y.__getitem__('summary'),
                                          assignee_team=y.__getitem__('Assignee Team'),
                                          sprint=y.__getitem__('sprint')
                                          )
                if 'resolved' in y.__dict__:
                    self.issues.add_issue(priority=y.__getitem__('Priority'), id=y.__getitem__('id'),
                                          stage=y.__getitem__('Stage'), spent_time=0,
                                          description=y.__getitem__('description') + '&nbsp;<br> (For more '
                                                                                     'information go to: '
                                                                                     'https://outer-heaven'
                                                                                     '.myjetbrains.com/youtrack'
                                                                                     '/issue/' + y.__getitem__('id')
                                                      + ')',
                                          resolved=y.__getitem__('resolved'),
                                          estimation=y.__getitem__('Estimation'), created=y.__getitem__('created'),
                                          assignee=y.__getitem__('Assignee'), summary=y.__getitem__('summary'),
                                          assignee_team=y.__getitem__('Assignee Team'),
                                          sprint=y.__getitem__('sprint')
                                          )
                else:
                    self.issues.add_issue(priority=y.__getitem__('Priority'), id=y.__getitem__('id'),
                                          stage=y.__getitem__('Stage'), spent_time=0,
                                          description=y.__getitem__('description') + '&nbsp;<br> (For more '
                                                                                     'information go to: '
                                                                                     'https://outer-heaven'
                                                                                     '.myjetbrains.com/youtrack'
                                                                                     '/issue/' + y.__getitem__('id')
                                          , resolved='',
                                          estimation=y.__getitem__('Estimation'), created=y.__getitem__('created'),
                                          assignee=y.__getitem__('Assignee'), summary=y.__getitem__('summary'),
                                          assignee_team=y.__getitem__('Assignee Team'),
                                          sprint=y.__getitem__('sprint')
                                          )
            except Exception as e:
                print('Error on getting issues[youtrack],', y.__getitem__('id'),',: ', e)
        print('Issues saved!')
        print('Getting relationships...')
        for y in (yt.getIssues('PEI', '', 0, 200)):
            for yy in yt.getIssue(y.__getitem__('id')).getLinks():
                    try:
                        if yy.typeOutward == 'is required for':
                            self.issues.add_parent(yy.source, yy.target)
                        if yy.typeOutward == 'relates to':
                            self.issues.add_related(yy.source, yy.target)
                    except Exception as e:
                        print('Error on getting relationships[youtrack]:,', y.__getitem__('id'),',: ', e)
        print('Relationships saved!')
        self.get_time_tracking()
        return self.issues

    def get_time_tracking(self):
        print('Getting time tracking...')
        for y in self.issues.issues.keys():
            try:
                for w in self.connection.getWorkItems(y):
                    try:
                        self.issues.issues.get(y).insert_time_tracking(w.__getitem__('description'),
                                                                       w.__getitem__('created'),
                                                                       w.__getitem__('url'), w.__getitem__('duration'),
                                                                       w.__getitem__('date'),
                                                                       w.__getitem__('author').__getitem__('login'),
                                                                       y,
                                                                       w.__getitem__('worktype').__getitem__('name'))
                    except Exception as e:
                        print('Error on working inserting time tracking on 2d[youtrack]: ', e)
            except Exception as e:
                print('Error on getting working items[youtrack]: ', e)
        print('Time tracking saved!')

