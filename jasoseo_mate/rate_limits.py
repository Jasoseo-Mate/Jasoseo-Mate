from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


def ai_rate_limit(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        limit = int(getattr(settings, "AI_RATE_LIMIT", 5))
        window = int(getattr(settings, "AI_RATE_LIMIT_WINDOW", 60))
        if limit <= 0:
            return view_func(request, *args, **kwargs)

        user_key = request.user.pk if request.user.is_authenticated else "anonymous"
        cache_key = f"ai-rate:user:{user_key}"
        if cache.add(cache_key, 1, timeout=window):
            request_count = 1
        else:
            try:
                request_count = cache.incr(cache_key)
            except ValueError:
                cache.set(cache_key, 1, timeout=window)
                request_count = 1

        if request_count > limit:
            response = JsonResponse(
                {
                    "status": "error",
                    "message": "AI 요청이 너무 많습니다. 잠시 후 다시 시도해 주세요.",
                },
                status=429,
            )
            response["Retry-After"] = str(window)
            return response

        return view_func(request, *args, **kwargs)

    return wrapped
