from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.list_blogs, name='list_blogs'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/<int:pk>/', views.retrieve_blog, name='retrieve_blog'),
    path('blogs/<int:pk>/update/', views.update_blog, name='update_blog'),
    path('blogs/<int:pk>/patch/', views.partial_update_blog, name='partial_update_blog'),
    path('blogs/<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    path('blogs/upload-image/',views.upload_blog_image, name='upload_blog_image'),

]

