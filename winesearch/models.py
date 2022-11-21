from django.db import models
from users.models import User
from wineceller.models import Wine
class Winesearch(models.Model):
    kname = models.CharField(max_length=300, null=False, blank=False, default='')
    wine_id = models.IntegerField(null=False, blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user')