from django.db import models
from users.models import User
from common.models import CommonModel
# Create your models here.


class WineCeller(CommonModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='winecellers')
    wine_id = models.IntegerField(null=True, blank=True)

    
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self)->str:
        return f"{self.owner}'s Wine Celler"

