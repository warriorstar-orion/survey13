from django.contrib import admin
from django.urls import path, include

from survey.views import (
    answers,
    characteristics,
    cohorts,
    participants,
    questions,
    root,
    sentiments,
)

urlpatterns = [
    path("", root.root),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("answers/", answers.answers),
    path("answers/<int:answer_id>/", answers.answer),
    path("answers/search/", answers.AnswerSearchResults.as_view(), name="answer_search_results"),
    path("answers/open_ended/", answers.OpenEndedListView.as_view()),
    path("characteristics/", characteristics.characteristics),
    path("characteristics/<int:characteristic_id>/", characteristics.characteristic),
    path("cohorts/", cohorts.cohorts),
    path("cohorts/<int:cohort_id>/", cohorts.cohort),
    path("participants/", participants.participants),
    path("participants/<int:participant_id>/", participants.participant),
    path("questions/", questions.questions),
    path("questions/open_ended/", questions.open_ended),
    path("questions/<int:question_id>/", questions.question),
    path("sentiments/", sentiments.sentiments),
    path("sentiments/<int:sentiment_id>/", sentiments.sentiment),
]
