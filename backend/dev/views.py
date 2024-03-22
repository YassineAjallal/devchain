import json
import os
import datetime
from web3 import Web3
from django.views import View
from .froms import CreateArticleForm, SetNameForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from moralis import auth

HOME = os.getenv('HOME')
load_dotenv(f'{HOME}/Desktop/devchain/.env')
API_KEY = os.getenv('API_KEY')
ARTICLES_CONTRACT_ADDRESS = os.getenv('ARTICLES_CONTRACT_ADDRESS')

with open(f'{HOME}/Desktop/devchain/blockchain/build/contracts/Articles.json', 'r') as article_abi:
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    abi = json.load(article_abi)['abi']
    article = web3.eth.contract(address=ARTICLES_CONTRACT_ADDRESS, abi=abi)


class Authenticate(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            encoded_address = web3.to_checksum_address(request.COOKIES['address'])
            user_name = article.functions.getUserName(encoded_address).call()
            if (len(user_name) == 0):
                return redirect('set name')
            response = redirect('home')
            response.set_cookie('name', user_name)
            return response
        return render(request, 'authenticate.html')


class SetName(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            form = SetNameForm()
            return render(request, 'set_name.html', {'form': form})
        return redirect('authenticate')

    def post(self, request):
        form = SetNameForm(request.POST)
        if form.is_valid() and 'address':
            if 'address' in request.COOKIES:
                tx_hash = article.functions.addUserName(form.data['your_name']).transact({'from': request.COOKIES['address']})
                web3.eth.wait_for_transaction_receipt(tx_hash)
                response = redirect('home')
                response.set_cookie('name', form.data['your_name'])
                return response
            return redirect('authenticate')
        return redirect('set name')


class Home(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            all_articles = article.functions.getAllArticles().call()
            print(all_articles)
            return render(request, 'home.html', {"name": request.COOKIES['name'], "articles": all_articles})
        else:
            return redirect('authenticate')
            

class CreateArticle(View):
    def get(self, request):
        if 'address' in request.COOKIES:
            create_article = CreateArticleForm()
            return render(request, 'create.html', {'create_form': create_article, "name": request.COOKIES['name']})
        return redirect('authenticate')

    def post(self, request):
        create_article = CreateArticleForm(request.POST)
        if create_article.is_valid():
            self.addArticleToBlockchain(request.COOKIES['address'], create_article.data['title'], create_article.data['content'])
            return redirect('home')
        return redirect('create article')
    
    def addArticleToBlockchain(self, address, title, content):
        ct = datetime.datetime.now()

        tx_hash = article.functions.addArticle(title, content, int(ct.timestamp())).transact({'from': address})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        encoded_address = web3.to_checksum_address(address)
        user_articles = article.functions.getArticles(encoded_address).call()
        all_articles = article.functions.getAllArticles().call()
        print(user_articles)
        print(all_articles)


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