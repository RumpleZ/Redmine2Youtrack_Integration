import json
import re

import youtrack2d


class Mapper:
    def __init__(self):
        self.map_KB_ST = {
            'Backlog': 1,  # 'New'
            'Develop': 2,  # 'In Progress'
            'Test': 3,  # 'Resolved'
            'Staging': 3,  # 'Resolved'
            'Review': 4,  # 'Feedback'
            'Done': 5  # 'Closed'
        }
        self.map_Stage = {
            'Backlog': 10,
            'Develop': 50,
            'Review': 60,
            'Test': 70,
            'Staging': 90,
            'Done': 100
        }
        self.map_Priority = {
            'Minor': 1,  # 'Low',
            'Normal': 2,  # 'Normal',
            'Major': 3,  # 'High',
            'Critical': 4,  # 'Urgent',
            'Show-stopper': 5  # 'Immediate',
        }
        self.map_Users = {
            'user': 00,
            }
        self.map_Activity = {
            'Management': 12,
            'Managementv2': 25,
            'Doc': 13,
            'Docv2': 14,
            'Dev': 15,
            'Testing': 16,
            'Research': 17,
            'Pitch': 18
        }
        self.map_Versions = {
            "1": 220,  # "Pitch Inicial",
            "2": 221,  # "Entrega I",
            "3": 222,  # "Pitch Academico",
            "4": 223,  # "Entrega II",
            "5": 224,  # "Pitch Final"
        }

        self.yt2rd = {}

    def map_engine(self, yt_struct, o):
        o.delete_issues()
        d = json.load(open("target_versions.json"))
        print('Importing issues...')
        for y in yt_struct.keys():
            issued_id = o.import_issues(status=self.map_KB_ST[yt_struct[y].__dict__['stage']],
                                        priority=self.map_Priority[yt_struct[y].__dict__['priority']], author=297,
                                        assignee=self.map_Users[yt_struct[y].__dict__['assignee']],
                                        start=yt_struct[y].__dict__['created'],
                                        due=int(yt_struct[y].__dict__['created']) + (int(
                                            yt_struct[y].__dict__['estimation']) * 60 * 3 * 1000),
                                        description=yt_struct[y].__dict__['description'].encode('ascii', 'ignore'),
                                        subject=(yt_struct[y].__dict__['summary']),
                                        estimation=int(yt_struct[y].__dict__['estimation']) / 60,
                                        targetV=self.map_Versions[str(d['targets'][str(y)])],
                                        done_ratio=self.map_Stage[yt_struct[y].__dict__['stage']])
            self.yt2rd[y] = str(issued_id)
            temp_sprint = yt_struct[y].__dict__['sprint']
            temp_assignee_team = yt_struct[y].__dict__['assignee_team']
            for yy in yt_struct[y].__dict__['time_tracking']:
                temp_worktype = yy.worktype
                o.import_time_tracking(issued_id, str(yy.__dict__['author']), float(yy.__dict__['duration']) / 60,
                                       self.willydros_logic(temp_assignee_team, temp_sprint, temp_worktype),
                                       yy.__dict__['description'].encode('ascii', 'ignore'), yy.__dict__['date'])

        print('Issues imported!\nImporting issues relationship...')
        for y in yt_struct.keys():
            if len(yt_struct[y].__dict__['parents']) != 0:
                try:
                    pass
                    # o.update_issue(y, yt_struct[y].__dict__['parents'][0], 'precedes')#, self.yt2rd[y])
                except Exception as e:
                    print('ERROR ON PARENTAGE: ', e)
        print('Issues relationship imported...')

    def willydros_logic(self, assignee_team, sprint, worktype):
        reg = re.compile('#(.*?) -')
        if worktype == 'Management':
            if assignee_team == 'Project Management':
                if int(re.findall(reg, str(sprint))[0]) == 1:
                    return self.map_Activity['Pitch']
                return self.map_Activity['Managementv2']
            return self.map_Activity['Management']
        if worktype == 'Documentation':
            if int(re.findall(reg, str(sprint))[0]) < 8:  # antes da sprint 8 vai para doc requis
                return self.map_Activity['Doc']
            return self.map_Activity['Docv2']
        if worktype == 'Development':
            return self.map_Activity['Dev']
        if worktype == 'Testing':
            return self.map_Activity['Testing']
        if worktype == 'Research':
            return self.map_Activity['Research']


import d2redmine

x = youtrack2d.Youtrack2csv().get_issues()

y = d2redmine.D2redmine()
w = Mapper()
w.map_engine(x.issues, y)
