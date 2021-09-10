from django.urls import path
from . import views


urlpatterns = [
    path("", views.view_blog, name="view_blog"),
    path("post/<int:post_id>/", views.view_post, name="view_post"),
]