from django.urls import path
from . import views

urlpatterns = [

    path('/similar_all/<int:wine_id>', views.SimilarWineListView().as_view())


]