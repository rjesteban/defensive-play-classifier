import json

PATH = 'data/actions/'


def load_action(gameid, eid):
    with open(PATH + str(gameid) + '.json') as f:
        data = json.load(f)
    ctx = data[str(eid)]
    action = Action(gameid=str(ctx['gameid']), eid=ctx['eventid'],
               coords=ctx['coords'], time=ctx['time'], quarter=ctx['quarter'],
               offense=ctx['offense'], defense=ctx['defense'],
               label=ctx['label'])
    return action


class Action(object):
    def __init__(self, gameid=None, eid=None, coords=None,
                 time=None, quarter=None,
                 offense=None, defense=None, label=None):
        self.eventid = eid
        self.coords = coords
        self.time = time
        self.quarter = quarter
        self.offense = offense
        self.defense = defense
        self.gameid = gameid
        self.label = label

    def save(self):
        context = {}
        context['eventid'] = self.eventid
        context['coords'] = self.coords
        context['time'] = self.time
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
