from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"), 
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('delete_image/<int:image_number>/', views.delete_image, name='delete_image'),

]
