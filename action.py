# def load():


class Action(object):

    def __init__(self, gameid, eventid, moment, home, away):
        self.eventid = eventid
        self.moment = moment
        self.home = home
        self.away = away
        self.gameid

    def save(self):
        context = {}
        context['eventid'] = self.eventid
        context['moment'] = self.moment
        context['home'] = self.home
        context['away'] = self.away
        context['gameid'] = self.gameid
        return context
