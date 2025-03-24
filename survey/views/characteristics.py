from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpRequest

from survey.models import Cohort, Participant, Characteristic


def characteristic(request: HttpRequest, characteristic_id):
    c = get_object_or_404(Characteristic, pk=characteristic_id)
    template = loader.get_template("characteristics/characteristic.html")
    context = {
        "characteristic": c,
    }

    return HttpResponse(template.render(context, request))


def characteristics(request: HttpRequest):
    characteristics = Characteristic.objects.all().order_by("id")
    template = loader.get_template("characteristics/index.html")
    context = {"characteristics": characteristics}
    return HttpResponse(template.render(context, request))
