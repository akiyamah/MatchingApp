from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from datetime import date
import os, random
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        print('###################### UserManager _create_user 起動')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        # Create UserProfile
        print('###################### Create UserProfile')
        unique_username = self.generate_random_username(email)
        UserProfile.objects.create(user=user, username=unique_username)
        
        # Create folder
        print('###################### Create folder')
        folder_path = os.path.join(settings.MEDIA_ROOT, f"user_profile/{user.id}")
        if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        return user

    @staticmethod
    def generate_random_username(email):
        username = email.split('@')[0]
        random_number = ''.join(str(random.randint(0, 9)) for _ in range(8))
        return f"{username}_{random_number}"

    def create_user(self, email, password=None, **extra_fields):
        print('###################### create_user 起動')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    # 認証情報
    email = models.EmailField(verbose_name=_("email"), unique=True)
    # ステータス管理情報
    is_superuser = models.BooleanField(verbose_name=_("is_superuser"), default=False)
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    
    current_year = date.today().year
    BIRTH_YEAR_CHOICES = [(year, year) for year in range(current_year - 20, 1949, -1)]
    BIRTH_MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    BIRTH_DAY_CHOICES = [(day, day) for day in range(1, 32)]
    
    GENDER_CHOICES = (
        ('未登録', '未登録'),
        ('M', '男性'),
        ('F', '女性'),
        ('O', 'その他'),
    )
    
    OCCUPATION_CHOICES = (
        ('未登録', '未登録'),
        ('IT業界', 'IT業界'),
        ('医療業界', '医療業界'),
        ('教育業界', '教育業界'),
        ('製造業', '製造業'),
        ('小売業', '小売業'),
        ('公務員', '公務員'),
        ('金融業界', '金融業界'),
        ('法律業界', '法律業界'),
        ('美容業界', '美容業界'),
        ('飲食業界', '飲食業界'),
        ('不動産業界', '不動産業界'),
        ('芸能・エンターテインメント業界', '芸能・エンターテインメント業界'),
        ('スポーツ選手', 'スポーツ選手'),
        ('その他', 'その他'),
    )
    
    ANNUAL_INCOME_CHOICES = (
        ('未登録', '未登録'),
        ('300万未満', '300万未満'),
        ('300-400万', '300-400万'),
        ('400-500万', '400-500万'),
        ('500-600万', '500-600万'),
        ('600-700万', '600-700万'),
        ('700-800万', '700-800万'),
        ('800-900万', '800-900万'),
        ('900-1000万', '900-1000万'),
        ('1000万以上', '1000万以上'),
    )
    
    def user_directory_path(instance, filename):
        return f"user_profile/{instance.user.id}/{filename}"
    
    # アプリ利用のためのユーザー詳細情報
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    birth_year = models.PositiveIntegerField(choices=BIRTH_YEAR_CHOICES, null=True, blank=True)
    birth_month = models.PositiveIntegerField(choices=BIRTH_MONTH_CHOICES, null=True, blank=True)
    birth_day = models.PositiveIntegerField(choices=BIRTH_DAY_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    occupation = models.CharField(max_length=30, choices=OCCUPATION_CHOICES, null=True, blank=True)
    annual_income = models.CharField(max_length=20, choices=ANNUAL_INCOME_CHOICES, null=True, blank=True)
    goals = models.ManyToManyField(Goal, blank=True)
    preferred_areas = models.ManyToManyField(Area, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    introduction = models.CharField(max_length=150, null=True, blank=True)
    profile_image1 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    profile_image2 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    profile_image3 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    profile_image4 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    profile_image5 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    def __str__(self):
        return self.username







class ProfileImage(models.Model):
    UPLOAD_SOURCE_CHOICES = (
        ('form1', 'Form 1'),
        ('form2', 'Form 2'),
        ('form3', 'Form 3'),
        ('form4', 'Form 4'),
        ('form5', 'Form 5'),
    )
    def user_directory_path(instance, filename):
        return f"user_profile/{instance.user_profile.user.id}/{filename}"
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    upload_source = models.CharField(max_length=10, choices=UPLOAD_SOURCE_CHOICES, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Profile Images"
    
