from .auth import decode_access_token

def check_if_token_is_valid(func):
    def wrapped_func(token, *args, **kwargs):
        decoded_token = decode_access_token(token)
        if decoded_token.get('error'):
            return decoded_token
        return func(token=decoded_token, *args, **kwargs)
    
    return wrapped_func
