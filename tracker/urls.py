from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('food-diary/', views.food_diary, name='food_diary'),
    path('lookup-food/', views.lookup_food, name='lookup_food'),
    path('challenges/', views.challenges, name='challenges'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
]
