import re
import time
# from redmine.redmine import *
from redminelib import Redmine


class D2redmine:
    def __init__(self):  # , url, key):
        self.url = "**"

        self.key_admin = "*"
        self.server_admin = Redmine(self.url, key=self.key_admin)

        self.key_1 = "*"
        self.server_1 = Redmine(self.url, key=self.key_1)

        self.key_2 = "*"
        self.server_2 = Redmine(self.url, key=self.key_2)

        self.key_3 = "*"
        self.server_3 = Redmine(self.url, key=self.key_3)

        self.key_4 = "*"
        self.server_4 = Redmine(self.url, key=self.key_4)

        self.key_5 = "*"
        self.server_5 = Redmine(self.url, key=self.key_5)

        self.key_6 = "*"
        self.server_6 = Redmine(self.url, key=self.key_6)

        self.key_7 = "*"
        self.server_7 = Redmine(self.url, key=self.key_7)

        self.key_8 = "*"
        self.server_8 = Redmine(self.url, key=self.key_8)

        self.dict_users = {'*': 297, '*': 201, '*': 207, '*': 280, '*': 274, '*': 289,
                           '*': 291, '*': 279, '*': 294}

        self.map_Users = {
            '*': 297,
            '*': 201,
            '*': 207,
            '*': 280,
            '*': 274,
            '*': 289,
            '*': 291,
            '*': 279,
            '*': 294
        }

    def delete_issues(self):
        pass

    def import_issues(self, status, priority, author, assignee, start, due, description, subject, estimation, targetV,
                      done_ratio):
        # issue:
        # project_id - NO
        # tracker_id - NO
        # status_id - SURE
        # priority_id - SURE
        # subject - SURE
        # description - SURE
        # category_id - NO
        # fixed_version_id - SURE
        # assigned_to_id - SURE
        # estimated_hours - SURE

        self.server_admin = Redmine(self.url, key=self.key_admin)
        issue = None
        try:
            issue = self.server_admin.issue.create(project_id='grupo-4', status_id=status, priority_id=priority,
                                                   author=297, assigned_to_id=assignee,
                                                   start_date=time.strftime('%Y-%m-%d', time.localtime(
                                                       int(str(start)) / 1000)),
                                                   due_date=time.strftime('%Y-%m-%d',
                                                                          time.localtime(int(str(due)) / 1000)),
                                                   estimated_hours=estimation, fixed_version_id=targetV,
                                                   description=str(description.replace('\n', '&nbsp;<br>')),
                                                   subject=str(subject), assignee=assignee, done_ratio=done_ratio
                                                   )
        except Exception as e:
            print('Error on issue creation[redmine]: ', e)

        return issue.id

    def update_issue(self, issued_id, parent_id, relation_type):
        return NotImplementedError

    def update_issue_related(self):
        return NotImplementedError

    def import_time_tracking(self, id, author, hours, activity, comments, date):
        self.switch(self.map_Users[author])

        self.server_admin.time_entry.create(issue_id=id, author=author, hours=hours, activity_id=activity,
                                            comments=comments,
                                            spent_on=time.strftime('%Y-%m-%d', time.localtime(int(str(date)) / 1000)))
        self.server_admin = Redmine(self.url, key=self.key_admin)

    def switch(self, author):
        if author == 297:
            self.server_admin = Redmine(self.url, key=self.key_admin)
        if author == 201:
            self.server_admin = Redmine(self.url, key=self.key_2)
        if author == 207:
            self.server_admin = Redmine(self.url, key=self.key_3)
        if author == 280:
            self.server_admin = Redmine(self.url, key=self.key_5)
        if author == 274:
            self.server_admin = Redmine(self.url, key=self.key_8)
        if author == 289:
            self.server_admin = Redmine(self.url, key=self.key_6)
        if author == 291:
            self.server_admin = Redmine(self.url, key=self.key_7)
        if author == 279:
            self.server_admin = Redmine(self.url, key=self.key_4)
        if author == 294:
            self.server_admin = Redmine(self.url, key=self.key_1)
