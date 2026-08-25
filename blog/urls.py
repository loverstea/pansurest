from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('register/', views.register, name='register'),

    path('photo/delete/<int:pk>/', views.delete_photo, name='delete_photo'),
    path('photo/edit/<int:pk>/', views.edit_photo, name='edit_photo'),

    path('user/<str:username>/', views.profile, name='profile'),

    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),

    path("photo/<int:photo_id>/rate/", views.rate, name="rate"),
]