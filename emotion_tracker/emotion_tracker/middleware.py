from django.http import HttpResponseNotFound


class SuperuserAdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_admin_path = request.path_info == '/admin' or request.path_info.startswith('/admin/')
        if is_admin_path and request.user.is_authenticated:
            if not request.user.is_active or not request.user.is_superuser:
                return HttpResponseNotFound()
        return self.get_response(request)