from django.http import JsonResponse
import os
class APIMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if  'token' in request.headers:
            if request.headers["Token"] == os.environ["THEWEBAPIKEY"]:
                response = self.get_response(request)
                return response
            else:
                JsonResponse({"Token": "You are using an invalid token"})
        else:
            return JsonResponse({"Token": "You Have No token header"})