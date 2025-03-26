from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostsAPIViewSet, basename="posts")
router.register('comments', views.PostCommentsAPIViewSet, basename="comments")

# app_name = 'posts'

urlpatterns = [
    path('', views.api_test),
    # path('posts/', views.get_post_list),
    # path('posts/', views.PostsAPI.as_view()),
    # path('posts/<int:pk>/', views.PostDetailAPI.as_view()),
    # path('posts/<int:pk>/comments/', views.PostCommentsAPI.as_view()),
    path('', include(router.urls))
]
