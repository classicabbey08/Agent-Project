from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('tenant', 'I am looking to rent'),
    ('agent',  'I am an agent / landlord'),
]

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='tenant',
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']