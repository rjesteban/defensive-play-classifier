import json

PATH = 'data/actions/'


def load_action(gameid, eid):
    with open(PATH + str(gameid) + '.json') as f:
        data = json.load(f)
    ctx = data[str(eid)]
    a = Action(str(ctx['gameid']), ctx['eventid'], ctx['coords'],
               ctx['offense'], ctx['defense'], ctx['label'])
    a.coords = ctx['coords']
    a.time = ctx['time']
    return a


def format_time(time):
    if isinstance(time, list):
        time = 1
    mins = int(time / 60)
    secs = int(((time / 60.0) - mins) * 60)
    return str(mins) + ':' + str(secs)


class Action(object):

    def __init__(self, gameid, eid, moment, offense, defense, label):
        self.eventid = eid
        if moment is None:
            self.coords = None
            self.time = None
        else:
            self.time = [format_time(time[2]) for time in moment]
            self.coords = [coord[5] for coord in moment]
        self.quarter = moment[0][0]  # to be used for transform wlog fxn
        self.offense = offense
        self.defense = defense
        self.gameid = gameid
        self.label = label

    def save(self):
        context = {}
        context['eventid'] = self.eventid
        context['time'] = self.time
        context['coords'] = self.coords
        context['quarter'] = self.quarter
        context['offense'] = self.offense
        context['defense'] = self.defense
        context['gameid'] = self.gameid
        context['label'] = self.label
        try:
            with open(PATH + str(self.gameid) + '.json', 'r') as f:
                data = json.load(f)
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                data[str(context['eventid'])] = context
                json.dump(data, f)
        except Exception:
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                json.dump({str(context['eventid']): context}, f)
        return context
