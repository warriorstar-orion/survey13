from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.db.models import Count

from survey.models import Question, Answer
from survey.forms import QuestionForm

def questions(request):
    questions = Question.objects.order_by("id")
    template = loader.get_template("questions/index.html")

    context = {
        "questions": questions,
    }
    return HttpResponse(template.render(context, request))

def open_ended(request):
    questions = Question.objects.filter(kind=Question.QuestionKind.OPEN_ENDED).order_by("id")
    template = loader.get_template("questions/index.html")

    context = {
        "questions": questions,
    }
    return HttpResponse(template.render(context, request))
    

def question(request, question_id):
    answers = Answer.answered().filter(question_id=question_id)

    context = {}
    if "unsentimented" in request.GET:
        context["unsentimented"] = request.GET.get("unsentimented")
        answers = answers.annotate(num_sentiments=Count("sentiments")).filter(num_sentiments__lt=1)


    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
        else:
            raise RuntimeError(form.errors.as_text())
    
    template = loader.get_template("questions/question.html")
    form = QuestionForm(instance=question)

    context["question"] = question
    context["answers"] = answers
    context["form"] = form
    return HttpResponse(template.render(context, request))
