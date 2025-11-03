from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
import time


class SimpleRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{client_ip}"
        
        requests = cache.get(cache_key, [])
        now = time.time()
        
        # Remove old requests outside the window
        requests = [req_time for req_time in requests if now - req_time < settings.RATE_LIMIT_WINDOW]
        
        if len(requests) >= settings.RATE_LIMIT_REQUESTS:
            return HttpResponse("Rate limit exceeded", status=429)
        
        requests.append(now)
        cache.set(cache_key, requests, settings.RATE_LIMIT_WINDOW)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
