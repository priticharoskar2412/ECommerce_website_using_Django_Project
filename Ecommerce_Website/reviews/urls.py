from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('product/<int:product_id>/reviews/add/', views.add_product_review, name='add_product_review'),
    path('product/<int:product_id>/reviews/detaill/',views.product_detaill,name='product_detaill'),
    ]
