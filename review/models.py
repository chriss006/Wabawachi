from django.db import models
from common.models import CommonModel
from users.models import User
from django.contrib.postgres.fields import ArrayField 
import datetime
# Create your models here.
    
class Review(CommonModel):
    class AssessmentChoice(models.TextChoices):
        good = ('좋음', '좋음')
        average = ('보통', '보통')
        bad = ('나쁨', '나쁨')
    #user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='review')
    #와인
    wine_id = models.IntegerField(null=False, blank=False, unique=True, default=0)
    #마신날짜
    date = models.DateField(blank=False, null=False,default=datetime.date.today)
    #선호도 평가
    assessment = models.CharField(max_length=20, choices=AssessmentChoice.choices, blank=False, null=False, default=AssessmentChoice.average)
    #해쉬태그
    hashtag = ArrayField(models.CharField(max_length=20), blank=False, default=list) 
    
    
    class Meta:
        db_table = "wine_celler_review"
        verbose_name = "와인 리뷰"
        verbose_name_plural = "와인 리뷰"