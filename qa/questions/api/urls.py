from django.urls import path, include
from rest_framework.routers import DefaultRouter
from qa.questions.api import views

router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet)

app_name = "api-question"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "questions/<slug:slug>/answer/",
        view=views.answer_create_view,
        name='answer-create'
    ),
    path(
        "questions/<slug:slug>/answers/",
        view=views.answer_list_view,
        name="answer-list"
    ),
    path(
        "answers/<int:pk>/",
        view=views.answer_rud_view,
        name="answer-detail"
    ),
    path(
        "answers/<int:pk>/like/",
        view=views.answer_like_view,
        name="answer-like"
    ),
]
