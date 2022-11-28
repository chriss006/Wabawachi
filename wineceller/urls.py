from django.urls import path
from . import views

urlpatterns = [

    path('/', views.WineCellerView().as_view()),
    path('/<int:wine_id>/detail', views.WineCellerDetailView.as_view())

]