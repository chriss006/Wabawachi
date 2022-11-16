from django.db import models
import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.TextChoices):
        MALE = ('male','Male')
        FEMALE = ('female', 'Female')
        OTHER = ('other', 'Other')
    
    class RegionChoices(models.TextChoices):
        경기도 = ('경기도', '경기')
        강원도 = ('강원도', '강원')
        충청북도 = ('충청북도', '충청북도')
        충청남도 = ('충청남도', '충청남도')
        전라북도 = ('전라북도', '전라북도')
        전라남도 = ('전라남도', '전라남도')
        경상북도 = ('경상북도', '경상북도')
        경상남도 = ('경상남도', '경상남도')
        제주특별자치도 = ('제주특별자치도','제주')
        서울특별시 = ('서울특별시', '서울')
        부산광역시 = ('부산광역시', '부산')
        인천광역시 = ('인천광역시', '인천')
        대구광역시 = ('대구광역시', '대구')
        광주광역시 = ('광주광역시','광주')
        울산광역시 = ('울산광역시','울산')
        세종특별시 = ('세종특별시', '세종')
    """
    customized User
    """
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    #custom
    email = models.EmailField(
        verbose_name=_('email id'),
        max_length=64,
        unique=True,
        help_text='EMAIL ID.'
    )
    username = models.CharField(
        max_length=30,
    )
    #birthdate
    birthdate = models.DateField(blank=False, null=False,default=datetime.date.today)
    #gender
    gender = models.CharField(
    max_length=10, choices=GenderChoices.choices, blank=False, null=False, default= GenderChoices.FEMALE
    )
    #address
    region = models.CharField(max_length=20, choices = RegionChoices.choices, blank=False, null=False,default=RegionChoices.서울특별시)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.email

