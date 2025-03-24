from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView
from django.db.models import Count
from django.db.models.functions import Length, Trim

from survey.models import Question, Answer
from survey.forms import AnswerForm

def answers(request):
    template = loader.get_template("root.html")
    return HttpResponse(template.render({}, request))

class OpenEndedListView(ListView):
    model = Answer
    template_name = "answers/index.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        if "unsentimented" in self.request.GET:
            result["unsentimented"] = self.request.GET.get("unsentimented")
        return result

    def get_queryset(self):
        unsentimented = self.request.GET.get("unsentimented")
        answers = (
            Answer.objects.annotate(
                num_sentiments=Count("sentiments"),
                trimmed_answer=Trim("answer_text"),
            )
            .exclude(trimmed_answer__exact="No Response")
            .exclude(trimmed_answer__iexact="No")
            .exclude(trimmed_answer__iexact="No?")
            .exclude(trimmed_answer__iexact="Yes")
            .exclude(trimmed_answer__iexact="Yes.")
            .exclude(trimmed_answer__iexact="No.")
            .exclude(trimmed_answer__iexact="Meh")
            .exclude(trimmed_answer__iexact="Good")
            .exclude(trimmed_answer__iexact="None")
            .exclude(trimmed_answer__iexact="Nope")
            .exclude(trimmed_answer__iexact="Nope.")
            .exclude(trimmed_answer__iexact="Nah")
            .exclude(trimmed_answer__iexact="idk")
            .exclude(trimmed_answer__iexact="eh")
            .exclude(trimmed_answer__iexact="ok")
            .exclude(trimmed_answer__iexact="")
            .exclude(trimmed_answer__iexact="-")
            .exclude(trimmed_answer__iexact="")
            .exclude(trimmed_answer__iexact="/")
            .exclude(trimmed_answer__iexact="n/a")
            .exclude(trimmed_answer__iexact="non")
            .exclude(trimmed_answer__iexact="null")
            .exclude(trimmed_answer__isnull=True)
        ).filter(participant__duplicate=False)
        if unsentimented:
            return answers.filter(
                question__kind=Question.QuestionKind.OPEN_ENDED,
                num_sentiments__lt=1,
            ).order_by(Length("answer_text").desc(), "id")

        return answers.filter(question__kind=Question.QuestionKind.OPEN_ENDED).order_by(
            Length("answer_text").desc(), "id"
        )


def answer(request: HttpRequest, answer_id):
    a = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        if not request.user.is_superuser:
            return

        form = AnswerForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
        else:
            raise RuntimeError(form.errors.as_text())
        return redirect(answer, answer_id=answer_id)

    template = loader.get_template("answers/answer.html")
    form = AnswerForm(instance=a)
    context = {
        "answer": a,
        "form": form,
        "is_superuser": request.user.is_superuser,
    }
    return HttpResponse(template.render(context, request))


class AnswerSearchResults(ListView):
    model = Answer
    template_name = "answers/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "q" in self.request.GET:
            context["q"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        objects = Answer.objects.filter(answer_text__icontains=query)
        if "unsentimented" in self.request.GET:
            objects = objects.annotate(num_sentiments=Count("sentiments")).filter(
                num_sentiments__lt=1
            )
        return objects
