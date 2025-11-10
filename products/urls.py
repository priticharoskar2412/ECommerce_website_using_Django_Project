from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Home or base view
    path('', views.home, name='home'),

    # Product and category listings
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryProductsView.as_view(), name='category_products'),

    # Product detail page (for linking from reviews)
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),


    # CRUD for products
    path('add/', views.ProductCreateView.as_view(), name='add_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
]
