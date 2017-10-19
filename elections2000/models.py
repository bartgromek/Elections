from django.db import models


class Voivodeship(models.Model):
    name = models.CharField(max_length=150, null=True, unique=True)
    abr = 'voiv'


class Constituency(models.Model):
    voivodeship = models.ForeignKey('Voivodeship', on_delete=models.CASCADE, null=True)
    name = models.IntegerField(default=0, unique=True)
    abr = 'cnst'


class Commune(models.Model):
    constituency = models.ForeignKey('Constituency', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, null=True, unique=True)
    abr = 'cmn'


class Result(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)


class District(models.Model):
    commune = models.ForeignKey('Commune', on_delete=models.CASCADE, null=True)
    name = models.IntegerField(default=0)
    cards = models.IntegerField(default=0)
    proper_votes = models.IntegerField(default=0)
    abr = 'dst'


class Candidate(models.Model):
    name = models.CharField(max_length=100, default='name')
