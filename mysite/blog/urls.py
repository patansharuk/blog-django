from django.urls import path, re_path
from .views import Blogs, SUDBlog, Comments, catch_all_view

urlpatterns = [
    path("",Blogs.as_view(),name="blogs_path"),
    # path("<int:blog_id>/edit",Blogs.edit,name="edit_blog_path"),
    # path("<int:blog_id>",Blogs.as_view(),name="blogs_path"),

    # path("<int:blog_id>/comments",Comments.index,name="blog_comments_path"),
    # path("<int:blog_id>/comment/create",Comments.create,name="create_comment"),
    # path("<int:blog_id>/comment/<int:comment_id>",Comments.as_view(),name="comments_path"),

    re_path(r'.*', catch_all_view),
]