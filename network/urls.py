
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.posts, name="index"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("following", views.following, name="following"),
    path('posts/new_comment/<int:post_id>', views.new_comment, name='new_comment'),
    path('posts/<int:post_id>', views.post, name='post'),
    path('users/<int:user_id>', views.user, name='user'),
    path('users/<int:user_id>/message', views.message, name='message'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
