from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField  
from common.models import CommonModel
# Create your models here.

class Wine(models.Model):
    
    wine_picture = models.URLField(null=False, blank=False)
    wine_id = models.IntegerField(null=False, blank=False, default=0)
    kname = models.CharField('와인명', max_length=100, null=False, blank=False)
    ename = models.CharField('winename', max_length=100, null=False, blank=False)
    winetype = models.CharField('winetype', max_length=10, null=False, blank=False)
    kr_country = models.CharField('국가명', max_length=50)
    kr_region = models.CharField('지역명', max_length=50)
    kr_grape_list = ArrayField(models.CharField(max_length=20), blank=True, default=list)  
    sweet = models.IntegerField('당도')
    acidic= models.IntegerField('산도')
    body = models.IntegerField('바디감')
    tannic = models.IntegerField('타닌감')
    notes_list =ArrayField(models.CharField(max_length=20), blank=True, default=list)  
    food_list = ArrayField(models.CharField(max_length=20), blank=True, default=list)  
    have_tried= models.BooleanField('먹어본 와인', null=False, blank=False, default=False )
    is_liked = models.BooleanField('찜한 와인',null=False, blank=False, default=False )


    def __str__(self):
        return f'{self.kname} / {self.ename}'


class WineCeller(CommonModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='winesellers')
    wine = models.ManyToManyField(Wine, related_name='winesellers')
    
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self)->str:
        return f"{self.owner}'s Wine Celler"
    
    def total_wine(wine, winetype):
        wines = wine.objects.get(winetype=winetype)
        return f'{winetype}: {wines.count()}개'
    
