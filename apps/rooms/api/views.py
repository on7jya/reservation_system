from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def test_html(request):
    return HttpResponse('testing html')

def test_json(request):
    pass
    # return JsonResponse(request)