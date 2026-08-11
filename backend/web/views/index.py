from django.shortcuts import render

from web.views.vite import get_vite_entry


def index(request):
    return render(request, 'index.html', get_vite_entry())
