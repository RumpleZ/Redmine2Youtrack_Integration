from IssueObject import IssueObject


class Issues:
    def __init__(self):
        self.issues = {}

    def add_issue(self, priority, stage, id, spent_time, description, resolved, estimation, created, assignee, summary,
                  assignee_team, sprint):
        self.issues[id] = \
            IssueObject(priority, stage, id, spent_time, description, resolved, estimation, created, assignee, summary,
                        assignee_team, sprint)

    def add_parent(self, issue_id, parent_id):
        self.issues[issue_id].insert_parent(parent_id)

    def add_related(self, issue_id, related_id):
        self.issues[issue_id].insert_related(related_id)

    def add_timetracking2issue(self, issue_id, description, created, url, duration, date, author, id, worktype):
        self.issues[issue_id].insert_time_tracking(description, created, url, duration, date, author, id, worktype)

    def add_comment2issue(self):
        return NotImplementedError

    def export2csv(self):
        return NotImplementedError

