
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    path("following", views.following, name="following"),
    path("new", views.new, name="new"),
    path("profile/<int:id>",views.profile, name="profile"),
    path("like", views.like, name="like"),
    path("editpost", views.editpost, name="editpost")
]