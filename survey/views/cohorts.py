from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpRequest

from survey.models import Cohort, Participant


def cohort(request: HttpRequest, cohort_id):
    c = get_object_or_404(Cohort, pk=cohort_id)
    template = loader.get_template("cohorts/cohort.html")
    participants = Participant.objects.filter(cohorts__id=cohort_id)
    context = {
        "cohort": c,
        "participants": participants,
    }

    return HttpResponse(template.render(context, request))


def cohorts(request: HttpRequest):
    cohorts = Cohort.objects.all().order_by("id")
    template = loader.get_template("cohorts/index.html")
    context = {"cohorts": cohorts}
    return HttpResponse(template.render(context, request))
