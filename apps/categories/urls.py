from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<slug:slug>/', views.CategoryArticleListView.as_view(), name='category_list'),
    path('<slug:slug>/<slug:sub_slug>/', views.CategoryArticleListView.as_view(), name='subcategory_list'),
    path('<slug:slug>/<slug:sub_slug>/<slug:subsub_slug>/', views.CategoryArticleListView.as_view(), name='subsubcategory_list'),
]
