from contextlib import nullcontext
from django.http import HttpRequest, HttpResponse, JsonResponse
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
import config

zbd_api_key = config.zbd_api_key

def index(request):
    """Paid scoreboard - All"""

    title = "A L L  S C O R E S  E V E R"
    score_list = Score.objects.filter(paid=True).order_by('-score_value')

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1
   
    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context)

def top(request, top):
    """Paid scoreboard - All"""
    title = "A L L  T I M E  T O P  " + str(top)
    score_list = Score.objects.filter(paid=True).order_by('-score_value')[:top]

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1
  
    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context)

def all(request):
    """Paid scoreboard - Top"""
    title = "A L L  S C O R E S  E V E R"
    score_list = Score.objects.filter(paid=True).order_by('-score_value')

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1
  
    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context) 


def event(request, event):
    """Paid scoreboard - Event All"""
    title = "A L L  S C O R E S @  - " + event.upper() 
    score_list = Score.objects.filter(paid=True).filter(event=event).order_by('-score_value')

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1
  
    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context)

def eventtop(request, event, top):
    """Paid scoreboard - Event Top"""

    title = "T O P  " + str(top) +  " @  - " + event.upper()
    score_list = Score.objects.filter(paid=True).filter(event=event).order_by('-score_value')[:top]

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1
  
    context = {
        'score_list': score_list,
        'title': title,
        'current_week': current_week,
        'last_week': last_week,
        'current_year': current_year
    }

    return render(request, 'viewScoreBoard.html', context=context)

def date(request, year, week):
    """Paid scoreboard - Date"""
    score_list = Score.objects.filter(score_date__year=year).filter(score_date__week=week).filter(paid=True).order_by('-score_value')

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1

    if week == current_week :

        title = "A L L  S C O R E S  -  C U R R E N T  W E E K "
        prize = "Prize Pool: 10,000 sats"

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

def datetop(request, year, week, top):
    """Paid scoreboard - Date"""
    
    score_list = Score.objects.filter(score_date__year=year).filter(score_date__week=week).filter(paid=True).order_by('-score_value')[:top]

    current_year = datetime.date.today().isocalendar()[0]
    current_week = datetime.date.today().isocalendar()[1]
    last_week = current_week - 1

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


class PaidAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated,)

    # 1. Update
    def post(self, request, *args, **kwargs):
        '''
        Update score with invoice payment status
        '''

        JSON = request.data
        
        score = Score.objects.get(id=JSON["id"])
        
        if score.twitter_handle == "":
        
            score.twitter_handle = JSON["twitter_handle"]
            score.event = JSON["event"]
            score.save()
            return Response(data=None, status=status.HTTP_202_ACCEPTED)

        else:
            return Response(data=None, status=status.HTTP_403_FORBIDDEN)


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