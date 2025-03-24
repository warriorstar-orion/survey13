from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Length, Trim

class Survey(models.Model):
    name = models.TextField()

    def __str__(self):
        return str(self.name)
    

class Characteristic(models.Model):
    name = models.TextField()

    def __str__(self):
        return str(self.name)


class Cohort(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self):
        return f"{self.characteristic}: {self.name}"


class Participant(models.Model):
    number = models.IntegerField(default=1)
    timestamp = models.DateTimeField("timestamp")
    cohorts = models.ManyToManyField(Cohort)
    duplicate = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Participant {self.pk}"
    
    def next_id(self):
        return Participant.objects.filter(id__gt=self.id).order_by('id').first().id
    
    def prev_id(self):
        return Participant.objects.filter(id__lt=self.id).order_by('-id').first().id


class QuestionCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return f"Question Category: {self.name}"


class Question(models.Model):
    class QuestionKind(models.TextChoices):
        UNSPECIFIED = "UNSPECIFIED", _("Unspecified")
        NUMERIC_RATING = "NUMERIC", _("Numeric Rating")
        SINGLE_CHOICE = "SINGLE_CHOICE", _("Single Choice")
        MULTIPLE_CHOICE = "MULTIPLE_CHOICE", _("Multiple Choice")
        OPEN_ENDED = "OPEN_ENDED", _("Open-ended")

    number = models.IntegerField(default=1)
    text = models.TextField()
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE)
    survey_column = models.CharField(max_length=3)
    categories = models.ManyToManyField(QuestionCategory)
    kind = models.CharField(choices=QuestionKind, default=QuestionKind.UNSPECIFIED, max_length=50)

    def next_id(self):
        return Question.objects.filter(id__gt=self.id).order_by('id').first().id
    
    def prev_id(self):
        return Question.objects.filter(id__lt=self.id).order_by('-id').first().id


    def __str__(self):
        return f"{self.survey.name} / Question {self.number}"


class SentimentCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return str(self.name)


class Sentiment(models.Model):
    summary = models.TextField()
    categories = models.ManyToManyField(SentimentCategory)

    def __str__(self):
        names = [x.name for x in self.categories.iterator()]

        return f"{', '.join(names)}: {self.summary}"


class Answer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    sentiments = models.ManyToManyField(Sentiment)

    def __str__(self):
        return str(self.answer_text)


    @classmethod
    def answered(cls):
        return cls.objects.annotate(trimmed_answer=Trim("answer_text")).exclude(trimmed_answer__exact="No Response")
