from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,RideViewSet
router = DefaultRouter()
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
path('', include(router.urls)),
]
