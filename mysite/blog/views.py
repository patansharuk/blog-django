from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.generic import TemplateView
from django.template import loader
from blog.models import Blog

class Blogs(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, self.template_name, {'blogs': blogs, 'message': f'found {len(blogs)} blogs'})

    def post(self, request):
        data_str = request.body.decode('utf-8')
        form_data = QueryDict(data_str)
        title = form_data.get('title')
        description = form_data.get('description')
        blog = Blog(title=title, description=description)
        blog.save()
        blogs = Blog.objects.all()
        return render(request, self.template_name, {'blogs': blogs, 'message': 'creating blog'})

class SUDBlog(Blogs):
    def get(self, request, blog_id):
        return render(request, 'base.html', {'message': 'viewing blog'})

    def put(self, request, blog_id):
        return render(request, 'base.html', {'message': 'updated blog'})

    def delete(self, request, blog_id):
        return render(request, 'base.html', {'message': 'deleted blog'})

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