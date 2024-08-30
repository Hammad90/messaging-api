from django.http import HttpResponsePermanentRedirect, HttpRequest
from django.utils.deprecation import MiddlewareMixin

class TrailingSlashMiddleware(MiddlewareMixin):
    def process_request(
            self,
            request: HttpRequest) -> HttpResponsePermanentRedirect:
        if not request.path.endswith('/'):
            if request.method in ['POST', 'PUT', 'PATCH']:
                return
            return HttpResponsePermanentRedirect(request.path + '/')
