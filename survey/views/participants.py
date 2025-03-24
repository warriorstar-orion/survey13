from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.db.models import Count

from survey.models import Answer, Participant
from survey.forms import ParticipantForm

def participants(request):
    participants = (
        Participant.objects.annotate(num_a=Count("answer"))
        .filter(num_a__gt=0)
        .filter(duplicate=False)
        .order_by("id")
    )
    template = loader.get_template("participants/index.html")
    context = {
        "participants": participants,
    }
    return HttpResponse(template.render(context, request))


def participant(request: HttpRequest, participant_id):
    p = get_object_or_404(Participant, pk=participant_id)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
        else:
            raise RuntimeError(form.errors.as_text())
        return redirect(participant, participant_id=participant_id)

    answers = Answer.objects.filter(participant_id=participant_id).order_by(
        "question_id"
    )
    template = loader.get_template("participants/participant.html")
    form = ParticipantForm(instance=p)

    context = {
        "participant": p,
        "answers": answers,
        "form": form,
    }
    return HttpResponse(template.render(context, request))

