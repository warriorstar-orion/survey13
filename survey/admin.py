from django.contrib import admin

# Register your models here.
from survey.models import (
    Answer,
    QuestionCategory,
    Characteristic,
    Cohort,
    Participant,
    Question,
    Sentiment,
    SentimentCategory,
)

admin.site.register(Answer)
admin.site.register(QuestionCategory)
admin.site.register(Characteristic)

admin.site.register(Question)
admin.site.register(Sentiment)
admin.site.register(SentimentCategory)


# class ParticipantInline(admin.TabularInline):
#     model = Participant

# class CohortAdmin(admin.ModelAdmin):
#     inlines = (ParticipantInline,)

admin.site.register(Cohort)
admin.site.register(Participant)
