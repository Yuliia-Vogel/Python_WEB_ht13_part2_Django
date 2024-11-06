from django.urls import path, include
from . import views

urlpatterns = [
    path("hello", views.hello, name="hello"),
    path('', views.quote_list, name='quote_list'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
]