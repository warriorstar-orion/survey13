from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.db.models import Count

from survey.models import Sentiment


def sentiment(request: HttpRequest, sentiment_id):
    s = get_object_or_404(Sentiment, pk=sentiment_id)
    template = loader.get_template("sentiments/sentiment.html")
    context = {
        "sentiment": s,
    }
    return HttpResponse(template.render(context, request))


def sentiments(request: HttpRequest):
    sentiments = (
        Sentiment.objects.annotate(num_answers=Count("answer"))
        .filter(answer__participant__duplicate=False)
        .order_by("-num_answers")
    )
    template = loader.get_template("sentiments/index.html")
    context = {"sentiments": sentiments}
    return HttpResponse(template.render(context, request))
