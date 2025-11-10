from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductReview
from products.models import Product  # Import Product model


def product_detail(request, pk):
    """This view is not needed if you already have one in products app."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def add_product_review(request, product_id):
    """Add a new review for a specific product."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Create and save review
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        # ✅ redirect to product detail page (in products app)
        return redirect('products:product_detail', pk=product.id)

    return render(request, 'reviews/add_review.html', {'product': product})


def product_reviews(request, product_id):
    """Show all reviews for a specific product."""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'reviews/review_list.html', {'product': product, 'reviews': reviews})
