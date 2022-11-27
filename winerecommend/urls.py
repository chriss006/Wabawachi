from django.urls import path
from . import views

urlpatterns = [

    path('/similar_all/<int:wine_id>', views.SimilarWineAllListView().as_view()),
    path('/similar_celler/<int:wine_id>', views.SimilarWineCellerListView.as_view())

]