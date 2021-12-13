#base frame code from class examples and django channels tutorial
from django.shortcuts import render, redirect

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Create your views here

from .import models
from . import forms


key = "8fe0d4cf-dfb7-4e3a-a75a-83c187d9affa"


def index(request):
    title = "Chat Room"
    context = {
        "title" : title
    }
    return render(request, "index.html",context = context)


#go to the chat room of choice
def room(request, room_name, userName):

    context =  {
        "room_name": room_name,
        "title": room_name,
        "userName":userName,

    }

    return render(request, "room.html", context)


def home(request):
    bodyContent = "From the Home Page"

    if(request.method == "POST"):
        myForm = forms.SuggestionForm(request.POST)
        if myForm.is_valid() and request.user.is_authenticated:
            myForm.save(request)
            myForm = forms.SuggestionForm()
            print("in here")
    else :
        myForm = forms.SuggestionForm()

    mySuggestionObjects = models.SuggestionModel.objects.all()
    suggestionList = []

    for suggest in mySuggestionObjects:
        commentOjects = models.CommentModel.objects.filter(
            suggestion = suggest
        )
        tempSugg = {}
        tempSugg["suggestionField"] = suggest.suggestionText
        tempSugg["id"] = suggest.id
        tempSugg["author"] = suggest.author.username
        tempSugg["comments"] = commentOjects
        tempSugg["publishedDate"] = suggest.datePublished

        #image not required so check first
        if suggest.image:
            tempSugg["image"] = suggest.image.url
            tempSugg["imageDescription"] = suggest.imageDescription
        else:
            tempSugg["image"] = ""
            tempSugg["imageDescription"] = ""


        suggestionList.append(tempSugg)
        print(str(len(commentOjects)) + " " +str(type(commentOjects)))
    content = {

        "title": "Home Crypto Community",
        "contentInfo": bodyContent,
        "myForm": myForm,
        "mySuggestion": suggestionList,
    }
    return render(request, "home.html", content)


def register(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()

    context = {
        "title": "Registration Page",
         "form": form
    }
    return render(request,"registration/register.html", context=context)



def commentView(request,sugg_id):

    if request.method == "POST":
        myForm = forms.CommentForm(request.POST)

        if myForm.is_valid() and request.user.is_authenticated:
            myForm.save(request, sugg_id)
            myForm = forms.CommentForm()

            return redirect("/")

    else:
        myForm = forms.CommentForm()


    context = {

        "title":"Comment",
        "body": "Comment Form",
        "form": myForm,
        "sugg_id": sugg_id,
    }

    return render(request, "comment.html", context)



def navBarHome(request):

    return render(request, "index.html")


def profitLoses(request):

    return render(request, "portfolio.html")

def memes(request):

    return render(request, "memes.html")


def suggestion(request):

    if(not request.user.is_authenticated):
        return redirect("/login/")

    if(request.method == "POST"):
        form = forms.SuggestionForm(request.POST, request.FILES)

        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/")
            #return render(request, "home.html")

    else:
        form = forms.SuggestionForm()


    context = {

        "title" : "Add Suggestion",
        "form":form
    }

    return render(request, "suggestion.html", context = context)


'''
    Skeleton code is provided by CoinMarketCap API.
    Recall we have a restriction on how many calls we can make daily. Thus for
    now we just focus on the top 10 cryptocurrency but this can be changed if
    we decide to upgrade to a higher package, which cost money
'''
def getStats(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5',#Free API Restriction
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key,
    }

    session = Session()
    session.headers.update(headers)

    dataList = []

    #new url for the logo, which is also provided by the coinmarketcap api
    logoUrl = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
    logoParameters = {
        "symbol": "",
        "aux": "logo"
    }

    logoSession = Session()
    logoSession.headers.update(headers)


    try:

        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        for dictElement in data["data"]:

            statsDict = {}

            statsDict["name"] = dictElement["name"]
            #fix the decimal format first
            price = dictElement["quote"]["USD"]["price"]
            price = round(price, 2)
            price = "{:,}".format(float(price))
            statsDict["price"] = price

            #fix the decimal format first
            marketCap = dictElement["quote"]["USD"]["market_cap"]
            marketCap = round(marketCap, 2)
            marketCap = "{:,}".format(float(marketCap))
            statsDict["marketCap"] = marketCap


            statsDict["symbol"] = dictElement["symbol"]
            statsDict["deltaOneDay"] = dictElement["quote"]["USD"]["percent_change_24h"]

            logoParameters["symbol"] = statsDict["symbol"]

            #call to get the logos

            logoResponse = logoSession.get(logoUrl, params = logoParameters)
            logoInfo = json.loads(logoResponse.text)
            statsDict["logo"] = logoInfo["data"][logoParameters["symbol"]]["logo"]
            #print("==== ", statsDict["logo"])

            #print(logoParameters["symbol"])

            dataList.append(statsDict)

            #print(dictElement["name"],  " ", symbol," ", price, " ", marketCap, " 24 hour change: ", deltaOneDay)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


    content = {

        "title": "Quick Stats",
        "data": dataList
    }

    return render(request, "stats.html", content)
