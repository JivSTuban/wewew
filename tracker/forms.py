from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, FoodEntry, UserChallenge
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Field('email', css_class='mb-3'),
            Field('password1', css_class='mb-3'),
            Field('password2', css_class='mb-3'),
            Submit('submit', 'Register', css_class='btn btn-success')
        )
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Field('password', css_class='mb-3'),
            Submit('submit', 'Login', css_class='btn btn-success w-100')
        )

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('current_weight', css_class='form-group col-md-4 mb-3'),
                Column('target_weight', css_class='form-group col-md-4 mb-3'),
                Column('daily_calorie_goal', css_class='form-group col-md-4 mb-3'),
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-success')
        )
    
    class Meta:
        model = UserProfile
        fields = ['target_weight', 'current_weight', 'daily_calorie_goal']

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['food_name', 'quantity', 'meal_type', 'calories', 'carbs', 'protein', 'fat', 'fiber']
        widgets = {
            'food_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food name',
                'required': True,
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Enter serving size'
            }),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter calories',
                'step': '0.01'
            }),
            'carbs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter carbs',
                'step': '0.01'
            }),
            'protein': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter protein',
                'step': '0.01'
            }),
            'fat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fat',
                'step': '0.01'
            }),
            'fiber': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fiber',
                'step': '0.01'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('food_name', wrapper_class='input-group', template='tracker/custom_field_with_button.html'),
                    css_class='form-group col-md-12 mb-3'
                ),
            ),
            Row(
                Column('quantity', css_class='form-group col-md-6 mb-3'),
                Column('meal_type', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('calories', css_class='form-group col-md-2 mb-3'),
                Column('protein', css_class='form-group col-md-2 mb-3'),
                Column('carbs', css_class='form-group col-md-2 mb-3'),
                Column('fat', css_class='form-group col-md-2 mb-3'),
                Column('fiber', css_class='form-group col-md-2 mb-3'),
            ),
            Submit('submit', 'Add Food Entry', css_class='btn btn-success')
        )
        # Make nutritional fields optional
        optional_fields = ['calories', 'carbs', 'protein', 'fat', 'fiber']
        for field in optional_fields:
            self.fields[field].required = False

        # Make these fields required
        required_fields = ['food_name', 'quantity', 'meal_type']
        for field in required_fields:
            self.fields[field].required = True

class UserChallengeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('challenge', css_class='mb-3'),
            Submit('submit', 'Start Challenge', css_class='btn btn-success')
        )

    class Meta:
        model = UserChallenge
        fields = ['challenge']
        widgets = {
            'challenge': forms.Select(attrs={'class': 'form-control'}),
        }
