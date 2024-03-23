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
        if 'address' in request.session:
            encoded_address = web3.to_checksum_address(request.session["address"])
            user_name = article.functions.getUserName(encoded_address).call()
            if (len(user_name) == 0):
                return redirect('set name')
            request.session['name'] = user_name
            return redirect('home')
        return render(request, 'authenticate.html')


class SetName(View):
    def get(self, request):
        if 'address' in request.session:
            form = SetNameForm()
            return render(request, 'set_name.html', {'form': form})
        return redirect('authenticate')

    def post(self, request):
        form = SetNameForm(request.POST)
        if form.is_valid() and 'address':
            if 'address' in request.session:
                tx_hash = article.functions.addUserName(form.data['your_name']).transact({'from': request.session["address"]})
                web3.eth.wait_for_transaction_receipt(tx_hash)
                request.session['name'] =  form.data['your_name']
                return redirect('home')
            return redirect('authenticate')
        return redirect('set name')


class Home(View):
    def get(self, request):
        if 'address' in request.session:
            all_articles = article.functions.getAllArticles().call()
            return render(request, 'home.html', {"name": request.session['name'], 'address': request.session['address'],"articles": all_articles})
        else:
            return redirect('authenticate')
          

class Logout(View):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        if 'logout' in request.POST:
            del request.session['name']
            del request.session['address']
        return redirect('home')


class ListUserArticles(View):
    def get(self, request):
        if 'address' in request.session:
            encoded_address = web3.to_checksum_address(request.session['address'])
            user_articles = article.functions.getArticles(encoded_address).call()
            return render(request, 'user_articles.html', {'articles': user_articles, 'name': request.session['name']})
        return redirect('authenticate')
    

class CreateArticle(View):
    def get(self, request):
        if 'address' in request.session:
            create_article = CreateArticleForm()
            return render(request, 'create.html', {'create_form': create_article, "name": request.session['name']})
        return redirect('authenticate')

    def post(self, request):
        create_article = CreateArticleForm(request.POST)
        if create_article.is_valid():
            self.addArticleToBlockchain(request.session["address"], create_article.data['title'], create_article.data['content'])
            return redirect('home')
        print(create_article.errors)
        return redirect('create')
    
    def addArticleToBlockchain(self, address, title, content):
        ct = datetime.datetime.now()
        tx_hash = article.functions.addArticle(title, content, int(ct.timestamp())).transact({'from': address})
        web3.eth.wait_for_transaction_receipt(tx_hash)


class ArticleDetails(View):
    def get(self, request, *args, **kwargs):
        if 'address' in request.session:
            found_article = article.functions.getArticleById(kwargs['id']).call()
            if found_article[0]:
                return render(request, 'article_details.html', {'article': found_article[1], 'name': request.session['name'], 'address': request.session['address']})
            return render(request, '404.html')
        return redirect('authenticate')


class Request(View):
    def get(self, request):
        return redirect('home')
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
    def get(self, request):
        return redirect('home')
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
        request.session["address"] = result['address']
        return HttpResponse(result)