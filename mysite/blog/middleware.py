from django.shortcuts import redirect,HttpResponse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and (request.path not in ['/blog/login', '/blog/logout', '/blog/notfound']):
            return redirect('not_found_path')
        response = self.get_response(request)
        return response
