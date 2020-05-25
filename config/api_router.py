from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from qa.users.api.views import UserViewSet
from qa.questions.alt_api.views import QuestionViewSet
from qa.questions.alt_api import views


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("questions", QuestionViewSet)


app_name = "api"

# urlpatterns = router.urls
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
