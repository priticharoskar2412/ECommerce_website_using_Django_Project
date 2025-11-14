from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.home,name='base.html'),
    path('products', views.ProductListView.as_view(), name='product_list'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # CRUD for products
    path('add/', views.ProductCreateView.as_view(), name='add_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),

    # Wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path("wishlist/add/<int:product_id>/", AddToWishlistView.as_view(), name="add_wishlist"),
    path("wishlist/remove/<int:product_id>/", RemoveFromWishlistView.as_view(), name="remove_wishlist"),
]
