from django.urls import path
from . import views
urlpatterns = [
    # path('add/', views.add_post, name = 'add_post'),
    path('add/', views.AddPost.as_view(), name = 'add_post'),
    # path('edit/<int:id>', views.edit_post, name = 'edit_post'),
    path('edit/<int:id>/', views.EditPost.as_view(), name = 'edit_post'),
    # path('delete/<int:id>', views.delete_post, name = 'delete_post'),
    path('delete/<int:id>/', views.DeletePost.as_view(), name = 'delete_post'),
]