from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('auth/refresh', TokenRefreshView().as_view()),
    path('auth/',views.AuthAPIView.as_view())
]
