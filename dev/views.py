import json
import requests
import os
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from dotenv import load_dotenv
from moralis import auth
from datetime import datetime, timezone, timedelta

load_dotenv()
API_KEY = os.getenv('WEB3_API_KEY')


# class MoralisAuth(View):
#     def get(self, request):
#         return render(request, 'login.html', {})

# class RequestMessage(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         print(data)
#         REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
#         request_object = {
#         "domain": "127.0.0.1",
#         "chainId": 1337,
#         "address": data['address'],
#         "statement": "Please confirm",
#         "uri": "http://127.0.0.1:8545",
#         "expirationTime": "2025-01-01T00:00:00.000Z",
#         "notBefore": "2023-01-01T00:00:00.000Z",
#         "timeout": 15
#         }
#         x = requests.post(
#             REQUEST_URL,
#             json=request_object,
#             headers={'X-API-KEY': API_KEY})
#         return JsonResponse(json.loads(x.text))

# class Profile(View):
#     def get(self, request):
#         return render(request, 'profile.html', {})

# class VerifyMessage(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         print(data)
#         REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
#         x = requests.post(
#             REQUEST_URL,
#             json=data,
#             headers={'X-API-KEY': API_KEY})
#         print(json.loads(x.text))
#         print(x.status_code)
#         if x.status_code == 201:
#             # user can authenticate
#             eth_address=json.loads(x.text).get('address')
#             print("eth address", eth_address)
#             try:
#                 user = User.objects.get(username=eth_address)
#             except User.DoesNotExist:
#                 user = User(username=eth_address)
#                 user.is_staff = False
#                 user.is_superuser = False
#                 user.save()
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     request.session['auth_info'] = data
#                     request.session['verified_data'] = json.loads(x.text)
#                     return JsonResponse({'user': user.username})
#                 else:
#                     return JsonResponse({'error': 'account disabled'})
#         else:
#             return JsonResponse(json.loads(x.text))

class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Request(View):
    def post(self, request):
        data = json.loads(request.body)
        body = {
        "domain": "127.0.0.1",
        "chainId": '1337',
        "address": data['address'],
        "statement": "Please confirm",
        "uri": "http://127.0.0.1:8545/",
        "expirationTime": "2025-01-01T00:00:00.000Z",
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 15
        }
        result = auth.challenge.request_challenge_evm(
            api_key=API_KEY,
            body=body
        )
        # print(type(result))
        return JsonResponse(result)

 
class Verify(View):
    def post(self, request):
        data = json.loads(request.body)
        
        body = {
            "message": data['message'],
            "signature": data['signature']
        }

        result = auth.challenge.verify_challenge_evm(
            api_key=API_KEY,
            body=body
        )
        return JsonResponse(result)