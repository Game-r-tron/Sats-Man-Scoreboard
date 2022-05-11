from rest_framework import serializers
from .models import Score
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["score_value", "score_date", "twitter_handle"]