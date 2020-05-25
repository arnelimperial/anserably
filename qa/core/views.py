from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse
from django.conf import settings

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if settings.DEBUG:
            template_name = "core/index-dev.html"
        else:
            template_name = "core/index.html"
        return template_name

main_core_view = IndexTemplateView.as_view()



