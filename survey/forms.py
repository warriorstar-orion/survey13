from django import forms

from survey.models import (
    Answer,
    Question,
    QuestionCategory,
    Participant,
    Cohort,
    Sentiment,
)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "kind"]

    text = forms.CharField(disabled=True)
    categories = forms.ModelMultipleChoiceField(
        queryset=QuestionCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["id", "cohorts"]

    id = forms.CharField(disabled=True)
    cohorts = forms.ModelMultipleChoiceField(
        queryset=Cohort.objects.all(), widget=forms.CheckboxSelectMultiple
    )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["id", "sentiments"]

    id = forms.CharField(disabled=True)
    sentiments = forms.ModelMultipleChoiceField(
        queryset=Sentiment.objects.all().order_by("categories", "summary"),
        widget=forms.CheckboxSelectMultiple,
    )
