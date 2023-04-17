from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 追加

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User