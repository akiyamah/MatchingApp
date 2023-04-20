from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginFrom, UserProfileForm
from .models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime
from django.views.generic import TemplateView
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.shortcuts import redirect
from .forms import (
    SignUpForm, UserProfileForm, 
)
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:index")
    
    def form_valid(self, form):
        print('##################### SignupView form_valid method 起動')
        # login after signup
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        
        # 追加: デバッグ用に User と UserProfile を出力
        print(f"##################### ユーザーが作成されました: {user}, UserProfile: {user.userprofile}")
        
        return response


class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"


class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")


class ProfileView(TemplateView):
    template_name = "profile.html"
    
    def get_user_data(self):
        user_data = UserProfile.objects.get(user=self.request.user)
        return user_data
    
    def get(self, request, **kwargs):
        print(f"###################### ProfileView GET method start, requst_user_id: {self.request.user.id} ")
        print()
        context = self.get_context_data(**kwargs)
        context['form'] = UserProfileForm(instance=self.get_user_data())
        return self.render_to_response(context)
    
    def post(self, request, **kwargs): 
        print('###################### ProfileView POST method start')
        
        user_data = self.get_user_data()
        form = UserProfileForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid():
            print('########################## ProfileView POST is_valid OK')
            user_profile = form.save(commit=False)
            user_profile.save()
            
            # ManyToManyFieldsの更新
            form.save_m2m()
            
            messages.success(request, 'プロフィールが更新されました。')
            context = self.get_context_data(**kwargs)
            context['form'] = UserProfileForm(instance=user_data)
            return self.render_to_response(context)
        else:
            print('########################## ProfileView POST is_valid FALSE')
            messages.error(request, 'プロフィールの更新に失敗しました。')
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
            return redirect('accounts:profile')

def delete_image(request, image_number):
    if 10 < image_number or image_number < 16:
        image_number = image_number - 10
        user_profile = request.user.userprofile
        image_field = getattr(user_profile, f'profile_image{image_number}')
        image_field.delete()
        user_profile.save()
        messages.success(request, '画像が削除されました。')
        return redirect('accounts:profile')
    else:
        messages.error(request, '無効な画像番号です。')
        return redirect('accounts:profile')

# ゴール：合コンで使用する、相手に閲覧される事を想定したユーザーのプロフィール詳細情報を閲覧、登録、更新、削除できる機能を実装すること。
# step1: 管理する対象のユーザー詳細情報を決定しモデルを作成する。
#        モデルを作成完了しました。これ以降のstepでは作成したモデルの内容を踏まえて作業を行って下さい。
# step2: フォームの構成を決定しformを作成する。
# 　　　　 各項目をどの様に表示させたいかの要件は以下のとおり。
#            "username": テキスト入力形式
#            "birth_year": 選択肢からプルダウン選択
#            "birth_month": 選択肢からプルダウン選択
#            "birth_day": 選択肢からプルダウン選択
#            "gender": 選択肢からプルダウン選択
#            "occupation": 選択肢からプルダウン選択
#            "annual_income": 選択肢からプルダウン選択
#            "goals": 選択肢からチェック式で複数選択
#            "preferred_areas": 選択肢からチェック式で複数選択
#            "hobbies": 選択肢からチェック式で複数選択
#            "profile_image1": 画像のアップロード
#            "profile_image2": 画像のアップロード
#            "profile_image3": 画像のアップロード
#            "profile_image4": 画像のアップロード
#            "profile_image5": 画像のアップロード
#        フォームを作成完了しました。これ以降のstepでは作成したモデルとフォーム内容を踏まえて作業を行って下さい。
# step3: ビュー機能を決定しビューを作成する。
#         ・プロフィール詳細情報を閲覧
#         　　GET method: リクエストユーザーのプロフィール詳細情報を取得し、初期値としてフォームにセットしたHTMLを返す。
#         ・プロフィール詳細情報を登録,更新
#         　　POST method: 受けっとった値をバリテーション後、DBに登録、更新する。その後、最新のリクエストユーザーのプロフィール詳細情報を取得し、フォームにセットしたHTMLを返す。
#         ・プロフィール詳細情報を削除
#         　　POST method: 削除処理は画像ファイルのデータに対してのみ機能を提供する。
# 　　　　　　　　　　　　　　　リクエストユーザーの受けっとった値をDBから削除する。その後、最新のリクエストユーザーのプロフィール詳細情報を取得し、フォームにセットしたHTMLを返す。

# それではProfileViewを再作成して下さい。





# step4: テンプレートで表示させたい構成を決定しテンプレートを作成する。

#           ただし、birth_year,birth_month,birth_dayは３つそれぞれにプルダウン選択ができるが、ユーザーの利便性のため３つ横並びで選択できる様にしたい。
