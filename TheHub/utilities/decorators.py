from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
import os
from .secrets import THEKEY


def check(func):
    def checking(*args, **kwargs):
        req = None
        for val in args:
            if isinstance(val,WSGIRequest):
                req = val
        if req:
            if req.headers["Token"] == THEKEY:
                return func(*args, **kwargs)
            else:
                return JsonResponse({"Error": "Token invalid"})
        else:
            raise Exception("Invalid Function passed into decorator")
    return checking

def valid_func_method(method):
    def check_method(func):
        def validate_method(*args,**kwargs):
            req = None
            for val in args:
                if isinstance(val, WSGIRequest):
                    req = val
            if  req:
                if req.method == method:
                    return func(*args, **kwargs)
                else:
                    return JsonResponse({"Error": f'Send {method} request'})
            else:
                raise Exception("Invalid Function passed into decorator")
        return validate_method
    return check_method

    
    