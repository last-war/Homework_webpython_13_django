from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('authors/', views.authors, name='authors'),
    path('detail/<int:author_id>', views.detail, name='detail'),
    path('fill_db/', views.fill_db, name='fill_db'),
]
