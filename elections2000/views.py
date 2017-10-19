from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elections2000.lib.data_parser import prepare_results
from .models import Result, District, Voivodeship, Constituency, Commune
from django.shortcuts import render, redirect
from elections2000 import serializers


def main_page(request):
    return render(request, 'results.html')


@api_view(['GET'])
def country_results(request):
    if request.method == 'GET':
        raw_results = Result.objects.all()
        districts = District.objects.all()
        header = 'Results in the Republic of Poland'
        results_package = prepare_results(districts=districts, results=raw_results, header=header)
        return HttpResponse(results_package.to_json())

@api_view(['GET'])
def voivodeships(request):
    if request.method == 'GET':
        voivodeships = Voivodeship.objects.all()
        serializer = serializers.VoivSerializer(voivodeships, many=True)
        return Response(serializer.data)