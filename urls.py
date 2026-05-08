
from django.urls import path
from .views import RouteOptimizationAPIView

urlpatterns = [
    path('optimize-route/', RouteOptimizationAPIView.as_view()),
]
