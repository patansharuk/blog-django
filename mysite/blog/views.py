from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.views.generic import TemplateView
from django.template import loader
from blog.models import Blog
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.cache import cache_page

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description='Successful response',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description='Unauthorized',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        500: openapi.Response(
            description='Internal server error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def hello_world_form(request):
    return Response({'message': 'Hello, World!'})

def get_request_messages(request, message=''):
    msgs = messages.get_messages(request)
    notice = ''
    for msg in msgs:
        notice += str(msg)
    if(notice != ''):
        message = notice
    return message

def get_pagination_object(items={}, page_number=1, items_per_page=10):
    p = Paginator(items, items_per_page)
    # current page details
    page = p.page(page_number)
    page_items = page.object_list
    # prev page details
    has_prev = page.has_previous()
    prev_page_number = int(page_number) - 1
    if(has_prev):
        prev_page_number = page.previous_page_number()
    # next page details
    has_next = page.has_next()
    next_page_number = int(page_number) + 1
    if(has_next):
        next_page_number = page.next_page_number()

    context = {'has_next': has_next, 'has_prev': has_prev, 'prev_page_number': prev_page_number, 'next_page_number': next_page_number,'page': page, 'page_items': page_items}
    return context

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

    @method_decorator(cache_page(60*1), name='get')
    def get(self, request):
        # fetch the blogs
        pgno = request.GET.get('pg') or 1
        blogs = Blog.objects.all()
        context = get_pagination_object(blogs, pgno, 3)

        msg = f'found {len(blogs)} blogs'
        message = get_request_messages(request, msg)
        context = {**context, 'message': message}

        return render(request, self.template_name, context)

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