from django.urls import path
from . import views

urlpatterns = [
    path('/', views.SearchView.as_view()),
    path('/detail/<int:wine_id>', views.SearchDetailView().as_view()),
    path('/<int:wine_id>/addWine', views.AddWineCellerView().as_view()),
    path('/recentwinesearch', views.RecentSearchedWineView().as_view())


]
