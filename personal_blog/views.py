from django.shortcuts import render
from posts.models import Post
from categories.models import Category

def home(request):
    data = Post.objects.all()
    return render(request, 'home.html', {'data': data})

def home(request):
    # Get all categories for the filter form (optional if you want to display them in a filter form)
    categories = Category.objects.all()

    # Check if a category filter is passed in the GET parameters
    category_id = request.GET.get('category')  # Get the selected category ID from URL query params
    if category_id:
        # If a category is selected, filter posts by that category
        data = Post.objects.filter(category__id=category_id)
    else:
        # If no category is selected, show all posts
        data = Post.objects.all()

    # Render the home page with filtered data and available categories
    return render(request, 'home.html', {
        'data': data,
        'categories': categories,
    })

