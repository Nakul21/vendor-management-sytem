import jwt
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.urls import resolve


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if Authorization header exists in the request
        # Check if the request URL matches the excluded endpoint
        if resolve(request.path_info).url_name == 'generate_token':
            # Skip authentication check for this endpoint
            return self.get_response(request)
        
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_header = request.META['HTTP_AUTHORIZATION']
            try:
                # Extract the token from the Authorization header
                token = auth_header.split()[1]
                
                # Decode the token
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                
                # Check if the token is expired
                if datetime.utcnow() > datetime.utcfromtimestamp(decoded_token['exp']):
                    return JsonResponse({"message": "Token has expired"}, status=401)
                
                # Check if the token contains the correct app name
                if decoded_token.get('app_name') != 'vendor_mgmt_sys':
                    return JsonResponse({"message": "Invalid token"}, status=401)

                # Token is valid, proceed with the request
                return self.get_response(request)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"message": "Invalid token"}, status=401)

        # Authorization header is missing, return 401 Unauthorized
        return JsonResponse({"message": "Authorization header is missing"}, status=401)
