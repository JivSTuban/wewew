from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import UserProfile, FoodEntry, Challenge, UserChallenge

# Custom admin classes
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_weight', 'target_weight', 'daily_calorie_goal')
    search_fields = ['user__username']

class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'calories', 'meal_type', 'date')
    list_filter = ('meal_type', 'date')
    search_fields = ['food_name', 'user__username']

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge_type', 'points', 'duration_days')
    list_filter = ('challenge_type',)
    search_fields = ['title']

class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'start_date', 'completed', 'completion_date')
    list_filter = ('completed', 'start_date')
    search_fields = ['user__username', 'challenge__title']

# Register models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FoodEntry, FoodEntryAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(UserChallenge, UserChallengeAdmin)

# Create Fitness Admin Group if it doesn't exist
try:
    fitness_admin_group = Group.objects.get(name='Fitness Admin')
except Group.DoesNotExist:
    fitness_admin_group = Group.objects.create(name='Fitness Admin')
    
    # Get content types
    challenge_content_type = ContentType.objects.get_for_model(Challenge)
    user_challenge_content_type = ContentType.objects.get_for_model(UserChallenge)
    
    # Define permissions for Fitness Admin
    challenge_permissions = Permission.objects.filter(
        content_type=challenge_content_type,
        codename__in=['add_challenge', 'change_challenge', 'view_challenge']
    )
    
    user_challenge_permissions = Permission.objects.filter(
        content_type=user_challenge_content_type,
        codename__in=['view_userchallenge']
    )
    
    # Add permissions to the group
    fitness_admin_group.permissions.set(list(challenge_permissions) + list(user_challenge_permissions))
