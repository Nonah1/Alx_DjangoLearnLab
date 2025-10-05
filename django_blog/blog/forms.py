# blog/forms.py
from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class PostForm(forms.ModelForm):
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

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='',
        help_text='Write your comment here.',
        max_length=2000
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content

