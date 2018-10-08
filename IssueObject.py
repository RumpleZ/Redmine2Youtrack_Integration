class IssueObject:
    class TimeTrackingObject:
        def __init__(self, description, created, url, duration, date, author, id, worktype):
            self.description = description
            self.created = created
            self.url = url
            self.duration = duration
            self.date = date
            self.author = author
            self.id = id
            self.worktype = worktype

    def __init__(self, priority, stage, id, spent_time, description, resolved, estimation, created, assignee, summary,
                 assignee_team, sprint):
        self.priority = priority
        self.stage = stage
        self.id = id
        self.spent_time = spent_time
        self.description = description
        self.resolved = resolved
        self.assignee_team = assignee_team
        self.sprint = sprint
        self.estimation = estimation
        self.created = created
        self.assignee = assignee
        self.summary = summary
        self.comments = []
        self.time_tracking = []
        self.parents = []
        self.related = []

    def insert_comment(self):
        return NotImplementedError

    def insert_parent(self, parent_id):
        self.parents.append(parent_id)

    def insert_related(self, related_id):
        self.related.append(related_id)

    def insert_time_tracking(self, description, created, url, duration, date, author, id, worktype):
        self.time_tracking.append(
            self.TimeTrackingObject(description, created, url, duration, date, author, id, worktype))
