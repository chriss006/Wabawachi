from django.urls import path
from . import views

urlpatterns = [

    path('/', views.WineCellerView().as_view()),
    path('/detail/<int:wine_id>', views.WineCellerDetailView.as_view()),
    path('/recentWines',views.RecentCollectedWineView.as_view()),
    path('/totalwines', views.WineCellerTotalView.as_view())

]