from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_weight = models.FloatField(null=True, blank=True)
    current_weight = models.FloatField(null=True, blank=True)
    daily_calorie_goal = models.IntegerField(default=2000)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class FoodEntry(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=200)
    calories = models.IntegerField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    fiber = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    calcium = models.FloatField(null=True, blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date = models.DateField(default=timezone.now)
    quantity = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"{self.food_name} - {self.meal_type} ({self.date})"

class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('food', 'Food Challenge'),
        ('workout', 'Workout Challenge'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    points = models.IntegerField(default=10)
    duration_days = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"
