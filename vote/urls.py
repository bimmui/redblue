from django.urls import path

from . import views

app_name = 'vote'

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('submitted/', views.submit, name='submit'),
    path('stats/', views.complete, name='complete'),
]