from django.urls import path
from . import views

urlpatterns = [

    path('/similar_all', views.SimilarWineAllListView().as_view()),
    path('/similar_celler', views.SimilarWineCellerListView.as_view()),
    path('/trending_wine', views.TrendingWineListView.as_view())

]