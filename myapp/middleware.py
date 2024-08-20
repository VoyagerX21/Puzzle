from django.utils.deprecation import MiddlewareMixin

class StaticCacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
