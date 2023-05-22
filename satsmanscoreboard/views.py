from contextlib import nullcontext
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import Score
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import ScoreSerializer
import requests, json
import datetime
import uuid
import datetime
import os

# TODO
# Event sepecific prizes into the Model
# Move API Views out into seperate class

#Import ZBD API key from environment.
try:
    zbd_api_key = os.environ["zbd_api_key"]
except KeyError as e:
    raise RuntimeError("Could not find a zbd_api_key in environment") from e

def get_dates():

    today = datetime.date.today().isocalendar()
    current_week = today[1]
    current_year = today[0]
    last_week = current_week - 1

    return current_year, current_week, last_week

# Passes all scrores to viewScoreBoard.html
def all(request):
    """Paid scoreboard - Top"""
    title = "A L L  S C O R E S  E V E R"
    score_list = Score.objects.filter(paid=True).order_by('-score_value')
  
    current_year, current_week, last_week = get_dates()

    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context) 

# Passes top x scrores to viewScoreBoard.html
def top(request, top):
    """Scoreboard - TOP"""
    title = "A L L  T I M E  T O P  " + str(top)
    score_list = Score.objects.filter(paid=True).order_by('-score_value')[:top]
  
    current_year, current_week, last_week = get_dates()

    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year,
    }

    return render(request, 'viewScoreBoard.html', context=context)

# Passes all scrores for a given 'event' URL parameter to viewEventScoreBoard.html
def event(request, event):
    """Scoreboard - Event All"""
    title = "A L L  S C O R E S @  - " + event.upper() 
    score_list = Score.objects.filter(paid=True).filter(event=event).order_by('-score_value')

    current_year, current_week, last_week = get_dates()

    #TODO Make this a DB/model thing
    if event == 'miami23':
        prize = "Prize Pool: 100,000 sats!"
    else:
        prize = "Prize Pool: 0 sats"
  
    context = {
        'score_list': score_list,
        'title': title,
        'prize': prize,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewEventScoreBoard.html', context=context)

# Passes top x scrores for a given 'event' URL parameter to viewEventScoreBoard.html
def eventtop(request, event, top):
    """Scoreboard - Event Top"""

    title = "T O P  " + str(top) +  " @  - " + event.upper()
    score_list = Score.objects.filter(paid=True).filter(event=event).order_by('-score_value')[:top]

    current_year, current_week, last_week = get_dates()

    #TODO Make this a DB/model thing
    if event == 'miami23':
        prize = "Prize Pool: 100,000 sats!"
    else:
        prize = "Prize Pool: 0 sats"
  
    context = {
        'score_list': score_list,
        'title': title,
        'prize': prize,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewEventScoreBoard.html', context=context)

# Passes all scrores for a given 'week' + 'year' URL parameter
# Current week to viewCurrentWeekScoreBoard.html
# Last week to viewLastWeekScoreBoard.html
# Any other week to viewScoreBoard.html
def date(request, year, week):
    """Paid scoreboard - Date"""
    score_list = Score.objects.filter(score_date__year=year, score_date__week=week, paid=True, event__isnull=True).order_by('-score_value')

    current_year, current_week, last_week = get_dates()

    if week == current_week :

        title = "A L L  S C O R E S  -  C U R R E N T  W E E K "
        prize = "Prize Pool: 10,000 sats"

        context = {
        'score_list': score_list,
        'title': title,
        'prize': prize,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
        }

        return render(request, 'viewCurrentWeekScoreBoard.html', context=context)

    elif week == last_week :

        title = "A L L  S C O R E S  -  L A S T  W E E K "

        context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year,
        }

        return render(request, 'viewLastWeekScoreBoard.html', context=context)

    else :

        title = "A L L  S C O R E S  I N  W E E K  " + str(week)
        
        context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
        }
        
        return render(request, 'viewScoreBoard.html', context=context)

# Passes top x scrores for a given 'week' + 'year' URL parameter
# Current week to viewCurrentWeekScoreBoard.html
# Last week to viewLastWeekScoreBoard.html
# Any other week to viewScoreBoard.html
def datetop(request, year, week, top):
    """Paid scoreboard - Date"""
    
    score_list = Score.objects.filter(score_date__year=year, score_date__week=week, paid=True, event__isnull=True).order_by('-score_value')[:top]

    current_year, current_week, last_week = get_dates()

    if week == current_week :

        title = "T O P  " + str(top) + "  -  C U R R E N T  W E E K "
        prize = "Prize Pool is 10,000 sats"

        context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year,
        'prize': prize
        }

        return render(request, 'viewCurrentWeekScoreBoard.html', context=context)

    elif week == last_week :

        title = "T O P  " + str(top) + "  -  L A S T  W E E K "

        context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year,
        }

        return render(request, 'viewLastWeekScoreBoard.html', context=context)

    else :

        title = "T O P  " + str(top) + "  S C O R E S  I N  W E E K  " + str(week)
        
        context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
        }
        
        return render(request, 'viewScoreBoard.html', context=context)

# Score entry screen. Called from within the game with a uniquie 'score_id' previously generated by API.
def enter_details(request, score_id):
    """Paid scoreboard - Enter details"""

    prize = "Prize Pool: 10,000 sats"

    current_year, current_week, last_week = get_dates()

    score_list = Score.objects.filter(score_date__year=current_year, score_date__week=current_week, paid=True, event__isnull=True).order_by('-score_value')

    
    if Score.objects.filter(id=score_id).exists():
    
        score = Score.objects.get(id=score_id).score_value
        
        context = {
            'score_id':score_id,
            'score_list':score_list,
            'score': score,
            'prize': prize
        }

        return render(request, 'enterUserDetails.html', context=context)

    else:

        return HttpResponseBadRequest("Score ID doesn't exist.")

# Score entry screen, pre-populating the 'even_code'. Called from within the game with a uniquie 'score_id' previously generated by API.
def enter_details_event(request, score_id, event_code):
    """Paid scoreboard - Enter details with Event Code"""

    if event_code == 'miami23':
        prize = "MIAMI23 Prize Pool: 100,000 sats!"
    else:
        prize = "Prize Pool: 0 sats"

    score_list = Score.objects.filter(event=event_code).filter(paid=True).order_by('-score_value')
    
    if Score.objects.filter(id=score_id).exists():
    
        score = Score.objects.get(id=score_id).score_value
        
        context = {
            'score_id':score_id,
            'score_list':score_list,
            'event_code':event_code,
            'score': score,
            'prize': prize
        }

        return render(request, 'enterEventUserDetails.html', context=context)

    else:

        return HttpResponseBadRequest("Score ID doesn't exist.")

#Main API for creating scores and getting ZBD invoice. Can get scores too.
class ScoreboardApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated,)

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the paid scores
        '''
        scores =  Score.objects.filter(paid=True).order_by('-score_value')
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a new score & get return invoice
        '''
            
        data = {
            'score_value': request.data.get('score_value'), 
        }

        serializer = ScoreSerializer(data=data)
        
        if serializer.is_valid():
            score = serializer.save()
            id = score.id.hex

            #Get Invoice from ZBD

            url = 'https://api.zebedee.io/v0/charges'
                        
            zbd_data = {
            "expiresIn": 3600,
            "amount": "1000000",
            "description": "Sats-Man Entry",
            "internalId": id,
            "callbackUrl": "https://games.gamertron.net/satsman-scoreboard/zbd"
            }

            headers = {'Content-type': 'application/json', 'apikey': zbd_api_key}
            response = requests.post(url, headers=headers, json=zbd_data)
            ZBDJsonResponse = response.json()

            score.bolt11_invoice = ZBDJsonResponse["data"]["invoice"]["request"]
            score.zbdId = ZBDJsonResponse["data"]["id"]
            score.save()

            unity_response = {
                "id": id,
                "bolt11_invoice": score.bolt11_invoice
            }

            return JsonResponse(unity_response, safe=False, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Callback API called when there is a sucessful ZBD payment
class ZBDAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    # 1. Update
    def post(self, request, *args, **kwargs):
        '''
        Update score with invoice payment status
        '''

        updateJSON = request.data
        print(updateJSON)
        ZBDstatus = updateJSON["status"]
        ZBDid = updateJSON["id"]
 
        score = Score.objects.get(zbdId=ZBDid)
        
        if ZBDstatus == "completed":
            score.paid = True
            score.save()
    
        return Response(data=None, status=status.HTTP_202_ACCEPTED)

#Adds player details to a given score.
class PaidAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    # 1. Update
    def post(self, request, *args, **kwargs):
        '''
        Update score with player details
        '''

        JSON = request.data
        score_id = JSON["id"]

        #Only allow 1 update for a known score ID
        if Score.objects.filter(id=score_id).exists():

            score = Score.objects.get(id=score_id)

            #Only allow a single update
            if score.updated:
            
                return Response(data=None, status=status.HTTP_403_FORBIDDEN)

            else:

                score.updated = True
                score.twitter_handle = JSON["twitter_handle"]
                score.npub = JSON["npub"]
                score.nip05 = JSON["nip05"]
                score.ln_address = JSON["ln_address"]
                score.event = JSON["event"]
                score.save()

            return Response(data=None, status=status.HTTP_202_ACCEPTED)

        else:
            return Response(data=None, status=status.HTTP_403_FORBIDDEN)

#Checks to see if an invoice has been paid.
class PaymentCheckAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated,)

    # 1. Check Payment Status
    def post(self, request, *args, **kwargs):
        '''
        Check payment status
        '''

        JSON = request.data
        
        score = Score.objects.get(id=JSON["id"])
        
        if score.paid == True:
        
            return Response(data=None, status=status.HTTP_200_OK)

        else:
            return Response(data=None, status=status.HTTP_402_PAYMENT_REQUIRED)