import json

from elections2000.management.commands.parse import canidates_results_template
from ..models import Candidate
from django.db.models import Sum


class ResultsPackage(object):
    #obw = -1
    header = ''
    #wynikiPk = {}
    #percentage_results = {}
    received_votes = {}
    proper_votes = 0
    cards = 0
    #first_place = 0
    #second_place = 0

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


def prepare_results(districts, results, header):
    try:
        proper_votes = districts.aggregate(Sum('proper_votes')).get('proper_votes__sum')
        cards = districts.aggregate(Sum('cards')).get('cards__sum')
    except:
        try:
            proper_votes = districts.proper_votes
            cards = districts.cards
        except:
            proper_votes = 0
            cards = 0
    received_votes = canidates_results_template.copy()
    for cn in received_votes:
        try:
            candidate = Candidate.objects.get(name=cn)
            candidate_results = results.filter(candidate=candidate)
            received_votes[cn] = candidate_results.aggregate(Sum('votes')).get('votes__sum')
        except:
            received_votes[cn] = 0
    data = {'proper_votes': proper_votes, 'cards': cards, 'header': header, 'received_votes': received_votes}
    #dane.update(dopieśćWyniki(otrzymaneGłosy, proper_votes))
    result = ResultsPackage(data)
    return result


"""
def dopieśćWyniki(wyniki, ważneGłosy):
    wynikiProcentowe = wyniki_kandydaci.copy()
    pierwszeMiejsce = 0
    drugieMiejsce = 0
    for kn in wyniki:
        if ważneGłosy == 0:
            wyniki[kn] = 0
        else:
            wynikiProcentowe[kn] = round((wyniki[kn] / ważneGłosy) * 100, 2)
        drugieMiejsce = max(min(pierwszeMiejsce, wynikiProcentowe[kn]), drugieMiejsce)
        pierwszeMiejsce = max(pierwszeMiejsce, wynikiProcentowe[kn])
    return {'pierwszeMiejsce': pierwszeMiejsce, 'drugieMiejsce': drugieMiejsce, 'percentageResults': wynikiProcentowe}
"""

"""
def wynikiId(wyniki):
    wnId = {}
    for wynik in wyniki:
        wnId[wynik.kandydat.imię_nazwisko] = wynik.pk
    return wnId
"""
