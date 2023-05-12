import uuid
from django.db import models

class Score(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score_value = models.IntegerField()
    score_date = models.DateTimeField(auto_now_add=True)
    twitter_handle = models.CharField(max_length=50,null=True)
    npub = models.CharField(max_length=50,null=True)
    ln_address = models.CharField(max_length=50,null=True)
    nip05 = models.CharField(max_length=50,null=True)
    bolt11_invoice = models.CharField(max_length=300)
    zbdId = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    event = models.CharField(max_length=20,null=True)
    updated = models.BooleanField(default=False,null=True)