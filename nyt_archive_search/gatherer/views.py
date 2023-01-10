from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm
import gatherer.gatherer as gt

def index(request):
    return render(request, 'gatherer/index.html')

def about(request):
    return render(request, 'gatherer/about.html')

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            
            c = form.cleaned_data

            return render(request, 'gatherer/display_results.html', c)
    else:
        form = SearchForm()

    return render(request, 'gatherer/search.html', {'form': form})


def display_results(request, keyword, start_date, end_date):
    return render(request, 'display_results.html', {'keyword': keyword, 'start_date': start_date, 'end_date': end_date})

def test_view(request, name):
    string = "Hello, " + name
    return HttpResponse(string)