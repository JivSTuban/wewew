# Generated by Django 5.1 on 2024-11-19 06:06

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('challenge_type', models.CharField(choices=[('food', 'Food Challenge'), ('workout', 'Workout Challenge')], max_length=20)),
                ('points', models.IntegerField(default=10)),
                ('duration_days', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='FoodEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=200)),
                ('calories', models.IntegerField()),
                ('carbs', models.FloatField()),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('fiber', models.FloatField()),
                ('sodium', models.FloatField()),
                ('calcium', models.FloatField()),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')], max_length=20)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('quantity', models.FloatField(default=1.0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_weight', models.FloatField(blank=True, null=True)),
                ('current_weight', models.FloatField(blank=True, null=True)),
                ('daily_calorie_goal', models.IntegerField(default=2000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
