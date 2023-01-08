from django.urls import path
from . import views

app_name = 'gatherer'
urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', view=views.about, name='about'),
    path('search/', views.search, name='search'),
    path('results/', view=views.results, name='results'),

]