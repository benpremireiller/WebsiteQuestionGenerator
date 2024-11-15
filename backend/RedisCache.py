from functools import wraps
import json


class APICache:

    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_expiry = 300  # 5 minutes

    def cache_response(self, func):
        """
        Get response from cache or make API call if not cached
        """

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Use the func name and args to get a unique key
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            
            # Try to get from cache
            cached = self.redis.get(cache_key)
            if cached:
                return cached
                
            # If not in cache, make the function call
            response = func(*args, **kwargs)
            
            # Cache the new response
            self.redis.setex(
                cache_key,
                self.default_expiry,
                json.dumps(response)
            )

            return response
            
        return wrapper