from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm
import gatherer

def index(request):
    return render(request, 'gatherer/index.html')

def about(request):
    return render(request, 'gatherer/about.html')

def search(request):
    if request.method == "POST":
        # pass form to gatherer
        # redirect to results page. 
        # display results. 
        form = SearchForm(request.POST)
        if form.is_valid():
            # results = gatherer.gatherer(request)
            
            # return redirect('results', results=form)
            return redirect('/gatherer/results/')

    
    form = SearchForm()
    return render(request, 'gatherer/search.html', {'form': form})

def results(request):
    # return render('gatherer/results.html', results)
    return HttpResponse("This is the results page.")