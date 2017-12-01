from .helpers import parse_date, get_coordinates
import re


class Match:
    def __init__(self, raw_data):
        self.raw = raw_data
        score1, score2, penalties = self._parse_scores()
        place = self._parse_place()
        match_type = self._parse_match_type()
        self.obj = {
            'equipos': [self.raw[0], self.raw[3]],
            'resultado': [score1, score2],
            'penales': penalties,
            'fecha': parse_date(self.raw[4]),
            'lugar': place,
            'tipo': match_type,
            'raw': self.raw[4]
        }
        self.includes_argentina = 'Argentina' in self.obj['equipos']
        if not self.includes_argentina:
            self.parse_national_raw()

    def _parse_scores(self):
        if '(' in self.raw[1]:
            team1_scores = re.findall('\d+', self.raw[1])
            score1 = int(team1_scores[0])
            penalty1 = int(team1_scores[1])

            team2_scores = re.findall('\d+', self.raw[2])
            score2 = int(team2_scores[0])
            penalty2 = int(team2_scores[1])

            penalties = [penalty1, penalty2]
        else:
            penalties = None
            score1 = int(self.raw[1])
            score2 = int(self.raw[2])
        return score1, score2, penalties

    def _parse_place(self):
        place = None
        if 'En' in self.raw[4]:
            place = self.raw[4].split('En ')[1].strip()
        return place

    def _parse_match_type(self):
        match_type = None
        if '-' in self.raw[4]:
            match_type = self.raw[4].split('-')[0].strip()
        return match_type

    def get_coordinates(self):
        if self.obj['lugar'] is not None:
            lat, long = get_coordinates(self.obj['lugar'])
            self.obj['lugar'] = {
                "raw": self.obj["lugar"],
                "lat": lat,
                "long": long
            }

    def parse_national_raw(self):
        before, after = self.obj['raw'].rsplit(' -')
        before = before.strip()
        rindex = before.rindex(' ')
        name = before[:rindex].strip()
        period = before[rindex + 1:].strip()
        if len(after) == 0:
            after = None
        else:
            after = after.strip()
        self.obj['torneo'] = {
            'nombre': name,
            'periodo': period,
            'contexto': after
        }
        del self.obj['raw']

    def __eq__(self, other):
        if isinstance(other, Match):
            if len(self.raw) == len(other.raw):
                return all([self.raw[i] == other.raw[i] for i in range(len(self.raw))])
        return False
