from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils import timezone
from .forms import UserRegisterForm, UserProfileForm, FoodEntryForm, UserLoginForm
from .models import UserProfile, FoodEntry, Challenge, UserChallenge
from .utils import fetch_food_data
import random
import json
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'tracker/login.html'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'tracker/profile.html', {'form': form})

@login_required
def food_diary(request):
    today = timezone.now().date()
    
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.date = today
            food_entry.save()
            messages.success(request, 'Food entry added successfully!')
            return redirect('food_diary')
    else:
        form = FoodEntryForm()
    
    entries = FoodEntry.objects.filter(user=request.user, date=today).order_by('meal_type')
    
    # Calculate totals
    totals = {
        'calories': sum((entry.calories or 0) * entry.quantity for entry in entries),
        'carbs': sum((entry.carbs or 0) * entry.quantity for entry in entries),
        'protein': sum((entry.protein or 0) * entry.quantity for entry in entries),
        'fat': sum((entry.fat or 0) * entry.quantity for entry in entries),
        'fiber': sum((entry.fiber or 0) * entry.quantity for entry in entries),
        'sodium': sum((entry.sodium or 0) * entry.quantity for entry in entries),
        'calcium': sum((entry.calcium or 0) * entry.quantity for entry in entries),
    }
    
    context = {
        'form': form,
        'entries': entries,
        'totals': totals,
        'date': today,
    }
    return render(request, 'tracker/food_diary.html', context)

@login_required
def challenges(request):
    user_challenges = UserChallenge.objects.filter(user=request.user)
    available_challenges = Challenge.objects.exclude(userchallenge__user=request.user)
    
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        action = request.POST.get('action')
        
        if action == 'start':
            challenge = Challenge.objects.get(id=challenge_id)
            UserChallenge.objects.create(user=request.user, challenge=challenge)
            messages.success(request, f'Started challenge: {challenge.title}')
        
        elif action == 'complete':
            user_challenge = UserChallenge.objects.get(id=challenge_id)
            user_challenge.completed = True
            user_challenge.completion_date = timezone.now().date()
            user_challenge.save()
            messages.success(request, f'Completed challenge: {user_challenge.challenge.title}')
    
    context = {
        'user_challenges': user_challenges,
        'available_challenges': available_challenges,
    }
    return render(request, 'tracker/challenges.html', context)

@login_required
def home(request):
    today = timezone.now().date()
    food_entries = FoodEntry.objects.filter(user=request.user, date=today)
    active_challenges = UserChallenge.objects.filter(user=request.user, completed=False)
    
    # Calculate daily totals
    daily_calories = sum(entry.calories * entry.quantity for entry in food_entries)
    calories_remaining = request.user.userprofile.daily_calorie_goal - daily_calories
    
    context = {
        'daily_calories': daily_calories,
        'calories_remaining': calories_remaining,
        'active_challenges': active_challenges,
    }
    return render(request, 'tracker/home.html', context)

@login_required
def lookup_food(request):
    """API endpoint to look up food nutritional information"""
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Only POST requests are allowed',
            'method': request.method
        }, status=405)
        
    try:
        data = json.loads(request.body)
        food_name = data.get('food_name', '').strip()
        
        if not food_name:
            return JsonResponse({
                'error': 'Food name is required',
                'received': data
            }, status=400)
            
        logger.info(f"Looking up food: {food_name}")
        nutrition_data = fetch_food_data(food_name)
        
        if not nutrition_data:
            return JsonResponse({
                'error': 'Food not found or API error occurred',
                'query': food_name
            }, status=404)
            
        logger.info(f"Found nutrition data for {food_name}: {nutrition_data}")
        return JsonResponse(nutrition_data)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        return JsonResponse({
            'error': 'Invalid JSON data',
            'details': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in lookup_food: {str(e)}")
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)
