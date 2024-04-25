from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.views.generic import TemplateView
from django.template import loader
from blog.models import Blog
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def get_request_messages(request, message=''):
    msgs = messages.get_messages(request)
    notice = ''
    for msg in msgs:
        notice += str(msg)
    if(notice != ''):
        message = notice
    return message

class Login(TemplateView):
    def get(self, request):
        message = get_request_messages(request)
        return render(request, 'login.html', {'message': message})

    def post(self, request):
        path = request.GET.get('next') or 'blogs_path'
        data_str = request.body.decode('utf-8')
        form_data = QueryDict(data_str)
        username = form_data.get('username')
        password = form_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Success :-)')
            return redirect(path)
        else:
            return render(request, 'login.html', {'message': 'Login Failed :-( Invalid details entered!','username':username,'password':password})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('log_path')

def not_found(request):
    return HttpResponse('this is not found page!')

class Blogs(TemplateView):
    template_name = 'home.html'

    @method_decorator(login_required(login_url="/blog/login"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        # fetch the blogs
        blogs = Blog.objects.all()
        msg = f'found {len(blogs)} blogs'
        message = get_request_messages(request, msg)

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
    @login_required(login_url='/blog/login')
    def create_blog(request):
        blog = Blog()
        return render(request, 'create.html',{'blog': blog})

    @login_required(login_url='/blog/login')
    def show_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        return render(request, 'show.html', {'blog': blog})

    @login_required(login_url='/blog/login')
    def edit_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        return render(request, 'edit.html', {'blog': blog})

    @login_required(login_url='/blog/login')
    def update_blog(request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        data_str = request.body.decode('utf-8')
        form_data = QueryDict(data_str)
        blog.title = form_data.get('title')
        blog.description = form_data.get('description')
        blog.save()
        return render(request, 'show.html', {'blog': blog})

    @login_required(login_url='/blog/login')
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