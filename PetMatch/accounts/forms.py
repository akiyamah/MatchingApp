from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Area, Goal, Hobby, UserProfile


User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        user = User.objects._create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        if commit:
            user.save()
        return user


# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'


class UserProfileForm(forms.ModelForm):
    birth_year = forms.ChoiceField(choices=UserProfile.BIRTH_YEAR_CHOICES, widget=forms.Select(attrs={'class': 'birth-date'}), required=False)
    birth_month = forms.ChoiceField(choices=UserProfile.BIRTH_MONTH_CHOICES, widget=forms.Select(attrs={'class': 'birth-date'}), required=False)
    birth_day = forms.ChoiceField(choices=UserProfile.BIRTH_DAY_CHOICES, widget=forms.Select(attrs={'class': 'birth-date'}), required=False)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, widget=forms.Select, required=False)
    occupation = forms.ChoiceField(choices=UserProfile.OCCUPATION_CHOICES, widget=forms.Select, required=False)
    annual_income = forms.ChoiceField(choices=UserProfile.ANNUAL_INCOME_CHOICES, widget=forms.Select, required=False)
    goals = forms.ModelMultipleChoiceField(queryset=Goal.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    preferred_areas = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    self_introduction = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    profile_image1 = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    profile_image2 = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    profile_image3 = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    profile_image4 = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    profile_image5 = forms.ImageField(required=False, widget=forms.ClearableFileInput())
    
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'birth_year',
            'birth_month',
            'birth_day',
            'gender',
            'occupation',
            'annual_income',
            'goals',
            'preferred_areas',
            'hobbies',
            'self_introduction',
            'profile_image1',
            'profile_image2',
            'profile_image3',
            'profile_image4',
            'profile_image5',
        ]

