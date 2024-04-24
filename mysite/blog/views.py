from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.views.generic import TemplateView
from django.template import loader
from blog.models import Blog
from django.contrib import messages

class Blogs(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        # fetch the blogs
        blogs = Blog.objects.all()
        message = f'found {len(blogs)} blogs'
        # handle notices
        msgs = messages.get_messages(request)
        notice = ''
        for msg in msgs:
            notice += str(msg)
        if(notice != ''):
            message = notice

        return render(request, self.template_name, {'blogs': blogs, 'message': message})

    def post(self, request):
        data_str = request.body.decode('utf-8')
        form_data = QueryDict(data_str)
        title = form_data.get('title')
        description = form_data.get('description')
        blog = Blog(title=title, description=description)
        blog.save()
        if(blog.id != None):
            messages.success(request, 'Blog created successfully')
        else:
            messages.success(request, 'Failed creating blog')
        return redirect('blogs_path')

class RevokeBlog(Blogs):
    def create_blog(request):
        blog = Blog()
        return render(request, 'create.html',{'blog': blog})

    def show_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        return render(request, 'show.html', {'blog': blog})

    def edit_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        return render(request, 'edit.html', {'blog': blog})

    def update_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        data_str = request.body.decode('utf-8')
        form_data = QueryDict(data_str)
        blog.title = form_data.get('title')
        blog.description = form_data.get('description')
        blog.save()
        return render(request, 'show.html', {'blog': blog})

    def delete_blog(request, blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
            blog.delete()
            if(blog.id == None):
                messages.success(request, 'Blog deleted successfully.')
            else:
                messages.success(request, 'Blog deletion failed.')
        except Exception as e:
            messages.success(request, e)
        return redirect('blogs_path')

class Comments(TemplateView):
    def index(request, blog_id):
        if request.method == 'GET':
            return HttpResponse('rendering the specific blog comments')
        else:
            return HttpResponse('invalid request type')

    def create(request, blog_id):
        if request.method == 'POST':
            return HttpResponse('creating the comment')
        else:
            return HttpResponse('invalid request type')
    
    def update(self, request, blog_id, comment_id):
        return HttpResponse(f'updating the comment {blog_id} {comment_id}')

    def delete(self, request, blog_id, comment_id):
        return HttpResponse(f'deleting the comment {blog_id} {comment_id}')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.delete(request, *args, **kwargs)
        else:
            return HttpResponse('request type is invalid!')


def catch_all_view(request):
    return HttpResponse('invalid path')