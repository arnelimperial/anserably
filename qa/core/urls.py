from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from qa.core.views import main_core_view


app_name = "core"
urlpatterns = [
    # re_path(r"^.*$", view=main_core_view, name="core-main"),
    path("", view=main_core_view, name="qa-app"),

]
