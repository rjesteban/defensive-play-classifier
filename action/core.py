import json

PATH = 'data/actions/'


def load(gameid):
    return json.load(open(PATH + str(gameid)))


def get_action(gameid, eid):
    return load(gameid)[str(eid)]


class Action(object):

    def __init__(self, gameid, eid, moment, offense, defense):
        self.eventid = eid
        self.coords = [coord[5] for coord in moment]
        self.quarter = moment[0][0]  # to be used for transform wlog fxn
        self.offense = offense
        self.offense = defense
        self.gameid = gameid

    def save(self):
        context = {}
        context['eventid'] = self.eventid
        context['coords'] = self.coords
        context['quarter'] = self.quarter
        context['offense'] = self.offense
        context['defense'] = self.defense
        context['gameid'] = self.gameid
        try:
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                data = json.load(f)
            data[str(context['gameid'])] = context
            json.dump(data, f)
        except Exception:
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                f.write({str(context['eventid']): context})
        return context
