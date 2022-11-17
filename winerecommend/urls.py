from django.urls import path
from . import views

urlpatterns = [

    path('/similar/<int:wine_id>', views.SimilarWineListView().as_view())


]