from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/profile.html"
