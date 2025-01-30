from django.urls import path
from . import views
from .views import create_application

urlpatterns = [
    path('', views.index, name='index'),
    path('Actions/', views.Actions, name='Actions'),
    path('catalog/', views.catalog, name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('project/', views.project, name='project'),
    path('Send/', views.Send, name='Send'),
    path('get_models/', views.get_models, name='get_models'),
    path('create-application/', create_application, name='create_application'),
]