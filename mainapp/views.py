from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Submissions, Exif

class IndexView(generic.ListView):
    model = Submissions

class DetailView(generic.DetailView):
    model = Submissions