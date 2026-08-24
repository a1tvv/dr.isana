from django.urls import path
from . import views

app_name = 'store'   # ← вот эта строка, скорее всего, отсутствует

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
]