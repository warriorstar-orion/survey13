from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect

def root(request):
    return redirect('/answers/', permanent=True)
