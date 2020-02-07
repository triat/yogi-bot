from django.shortcuts import render

from .models import Match


def home(request):
    matches = Match.objects.all()
    return render(request, "yogi_web/home.html", {"matches": matches})
