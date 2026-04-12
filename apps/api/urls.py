from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'articles', views.ArticleViewSet, basename='article')
router.register(r'terms', views.InteractiveTermViewSet, basename='term')

urlpatterns = [
    path('v1/', include(router.urls)),
]
