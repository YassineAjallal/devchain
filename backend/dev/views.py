import json
import requests
import os
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from dotenv import load_dotenv
from moralis import auth
from django.views.generic import RedirectView

load_dotenv()
API_KEY = os.getenv('WEB3_API_KEY')

class Authenticate(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            return redirect('home')
        return render(request, 'authenticate.html')



class Home(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            return render(request, 'home.html')
        else:
            return redirect('authenticate')
            

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
        return JsonResponse(result)

 
class Verify(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        
        body = {
            "message": data['message'],
            "signature": data['signature']
        }

        result = auth.challenge.verify_challenge_evm(
            api_key=API_KEY,
            body=body
        )
        response = HttpResponse(result)
        response.set_cookie("address", result['address'])
        return response