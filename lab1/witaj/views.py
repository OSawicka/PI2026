from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

def hello(request):
    return HttpResponse("Witaj w Django!")

def hello_name(request, name):
    return HttpResponse(f"Witaj, {name}!")

def hello_template(request, name):
    return render(request, "witaj/hello.html",
                  {"name": name})

def time_view(request):
    now = datetime.now()
    return render(request, "witaj/time.html", {"now": now})