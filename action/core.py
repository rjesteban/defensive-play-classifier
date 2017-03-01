import json

PATH = 'data/actions/'


def load(gameid):
    return json.load(open(PATH + str(gameid)))


def get_action(gameid, eid):
    return load(gameid)[str(eid)]


class Action(object):

    def set_params(self, gameid, eid, moment, offense, defense):
        self.eventid = eid
        self.coords = [coord[5] for coord in moment]
        self.quarter = moment[0][0]  # to be used for transform wlog fxn
        self.offense = offense
        self.defense = defense
        self.gameid = gameid


    # if action has json data already
    def load(self, gameid, eid):
        # context = json.load(open(PATH + str(gameid) + '.json'))
        with open(PATH + str(gameid) + '.json') as f:
            data = json.load(f)
        context = data[str(eid)]
        self.eventid = context['eventid']
        self.coords = context['coords']
        self.quarter = context['quarter']
        self.offense = context['offense']
        self.defense = context['defense']
        self.gameid = context['gameid']


    def save(self):
        context = {}
        context['eventid'] = self.eventid
        context['coords'] = self.coords
        context['quarter'] = self.quarter
        context['offense'] = self.offense
        context['defense'] = self.defense
        context['gameid'] = self.gameid
        data = {str(context['eventid']): context}
        try:
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                data = json.load(f)
                data[str(context['eventid'])] = context
                json.dump(data, f)
        except Exception:
            with open(PATH + str(self.gameid) + '.json', 'w') as f:
                json.dump(data, f)
        return context
