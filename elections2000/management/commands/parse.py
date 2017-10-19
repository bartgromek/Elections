import xlrd
from elections2000.models import Voivodeship, Commune, Constituency, Candidate, District, Result
from django.core.management.base import BaseCommand

# -*- coding: utf-8 -*-

candidates = ["Dariusz Maciej GRABOWSKI", "Piotr IKONOWICZ", "Jarosław KALINOWSKI",
              "Janusz KORWIN-MIKKE", "Marian KRZAKLEWSKI", "Aleksander KWAŚNIEWSKI",
              "Andrzej LEPPER", "Jan ŁOPUSZAŃSKI", "Andrzej Marian OLECHOWSKI",
              "Bogdan PAWŁOWSKI", "Lech WAŁĘSA", "Tadeusz Adam WILECKI"]

canidates_results_template = {'Dariusz Maciej GRABOWSKI': 0, "Piotr IKONOWICZ": 0, "Jarosław KALINOWSKI": 0,
                              "Janusz KORWIN-MIKKE": 0, "Marian KRZAKLEWSKI": 0, "Aleksander KWAŚNIEWSKI": 0,
                              "Andrzej LEPPER": 0, "Jan ŁOPUSZAŃSKI": 0, "Andrzej Marian OLECHOWSKI": 0,
                              "Bogdan PAWŁOWSKI": 0, "Lech WAŁĘSA": 0, "Tadeusz Adam WILECKI": 0}

voivs_constituency = {"Dolnośląskie": [1, 2, 3, 4], "Kujawsko-pomorskie": [5, 6, 7],
                      "Lubelskie": [8, 9, 10, 11, 12], "Lubuskie": [13, 14], "Łódzkie": [15, 16, 17, 18, 19],
                      "Małopolskie": [20, 21, 22, 23, 24, 25, 26, 27],
                      "Mazowieckie": [28, 29, 30, 31, 32, 33, 34, 35, 36],
                      "Opolskie": [37, 38], "Podkarpackie": [39, 40, 41, 42], "Podlaskie": [44, 45],
                      "Pomorskie": [46, 47, 48], "Śląskie": [49, 50, 51, 52, 53, 54], "Świętokrzyskie": [55, 56],
                      "Warmińsko-mazurskie": [57, 58, 59, ], "Wielkopolskie": [60, 61, 62, 63],
                      "Zachodniopomorskie": [65, 66, 67, 68]}

voivodeships = ["Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie", "Lubuskie", "Łódzkie",
                "Małopolskie", "Mazowieckie", "Opolskie", "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
                "Świętokrzyskie",
                "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"]


class Command(BaseCommand):
    @staticmethod
    def clean_db():
        Voivodeship.objects.all().delete()
        District.objects.all().delete()
        Constituency.objects.all().delete()
        Commune.objects.all().delete()
        Result.objects.all().delete()
        Candidate.objects.all().delete()

    @staticmethod
    def add_voivs():
        for v in voivodeships:
            Voivodeship(name=v).save()

    @staticmethod
    def add_candidates():
        for c in candidates:
            Candidate(name=c).save()

    @staticmethod
    def new_district(commune, number, cards, votes):
        return District(commune=commune, name=number, cards=cards, proper_votes=votes)

    def handle(self, *args, **options):

        self.clean_db()
        self.add_candidates()
        self.add_voivs()
        voiv_nr = 0
        for file in range(1, 69):  # iterate through xls files
            book = xlrd.open_workbook("elections2000/results/obwody/obw" + str(file).zfill(2) + ".xls")  # opening files
            sh = book.sheet_by_index(0)

            if voivs_constituency[voivodeships[voiv_nr]].count(file) == 0:
                voiv_nr += 1
            voiv_name = voivodeships[voiv_nr]
            voiv = Voivodeship.objects.filter(name=voiv_name).first()
            constituency = Constituency(name=file, voivodeship=voiv)
            constituency.save()
            for rx in range(1, sh.nrows):  # iterate through rows
                commune_name = str(sh.cell(rx, 2).value)
                communes = Commune.objects.filter(name=commune_name)
                if communes.count() == 0:
                    new_commune = Commune(name=commune_name, constituency=constituency)
                    new_commune.save()
                else:
                    new_commune = communes.first()

                district_nr = int(sh.cell(rx, 4).value)
                cards = int(sh.cell(rx, 8).value)
                votes = int(sh.cell(rx, 11).value)
                district = self.new_district(new_commune, district_nr, cards, votes)
                district.save()
                for cn in range(12, sh.row_len(rx)):  # iterate through candidates
                    candidate = Candidate.objects.get(name=str(sh.cell(0, cn).value))
                    votes = int(sh.cell(rx, cn).value)
                    Result(votes=votes, candidate=candidate, district=district).save()
