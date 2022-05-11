from django.http import HttpResponse
from django.shortcuts import render
from .models import Score
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import ScoreSerializer


def index(request):
    """View function for home page of site."""

    # Setup template variables
    number_of_scores = Score.objects.all().count()
    highest_score = Score.objects.all().order_by('-score_value')[:1]
    score_list_all = Score.objects.all().order_by('-score_value')
    score_list_top_3 = Score.objects.all().order_by('-score_value')[:3]
    score_list_top_10 = Score.objects.all().order_by('-score_value')[:10]
    #score_list_all_this_week = Score.objects.filter(pub_date__week=17).order_by('-score_value')

   
    context = {
        'number_of_scores': number_of_scores,
        'highest_score': highest_score,
        'score_list_all': score_list_all,
        'score_list_top_3' : score_list_top_3,
        'score_list_top_10' : score_list_top_10,
        #'score_list_all_this_week' : score_list_all_this_week
    }

    # Render the HTML template with the data in the context variable
    return render(request, 'viewScoreBoard.html', context=context)

class ScoreboardApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the scores
        '''
        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a new score
        '''
        data = {
            'score_value': request.data.get('score_value'), 
            'score_date': request.data.get('score_date'), 
            'twitter_handle' : request.data.get('twitter_handle'),   
        }
        serializer = ScoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)