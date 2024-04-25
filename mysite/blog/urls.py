from django.urls import path, re_path
from .views import Blogs, RevokeBlog, Comments, catch_all_view, login_user, logout_user, not_found

urlpatterns = [
    path("",Blogs.as_view(),name="blogs_path"),
    path("create",RevokeBlog.create_blog,name="create_blog_path"),
    path("<int:blog_id>/show",RevokeBlog.show_blog,name="show_blog_path"),
    path("<int:blog_id>/edit",RevokeBlog.edit_blog,name="edit_blog_path"),
    path("<int:blog_id>/update",RevokeBlog.update_blog,name="update_blog_path"),
    path("<int:blog_id>/destroy",RevokeBlog.delete_blog,name="delete_blog_path"),

    path("login",login_user,name="login_path"),
    path("logout",logout_user,name="logout_path"),
    path("notfound",not_found,name="not_found_path"),

    # path("<int:blog_id>/comments",Comments.index,name="blog_comments_path"),
    # path("<int:blog_id>/comment/create",Comments.create,name="create_comment"),
    # path("<int:blog_id>/comment/<int:comment_id>",Comments.as_view(),name="comments_path"),

    re_path(r'.*', catch_all_view),
]