from fastapi import Request
from functools import wraps

from .auth import decode_access_token

def check_if_token_is_valid(func):
    @wraps(func)
    def wrapped_func(request: Request, *args, **kwargs):
        token = request.cookies.get('access_token')
        if token:
            decoded_token = decode_access_token(token)
            if decoded_token.get('error'):
                return decoded_token
            
            return func(request=request, *args, **kwargs)
        else:
            return {'error': 'Авторизация не была пройдена'}
        
        
    
    return wrapped_func
