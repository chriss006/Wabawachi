from django.urls import path
from . import views

urlpatterns = [
    path('/', views.SearchView.as_view()),
    path('/<int:wine_id>', views.SearchDetailView().as_view()),
    path('/addWine', views.AddWineCellerView().as_view())


]
