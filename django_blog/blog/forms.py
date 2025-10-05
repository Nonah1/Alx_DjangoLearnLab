# blog/forms.py
from django import forms
from .models import Post, Profile, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class PostForm(forms.ModelForm):
 # tags input as comma-separated string
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags. Example: django, python, web',
        widget=forms.TextInput()
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

