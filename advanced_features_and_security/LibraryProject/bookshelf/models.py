from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError("The username field is required")
        user= self.model(username=username, email=email)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, username, email=None, paasword=None):
        extra_field.setdefault("is_admin", True)

        if extra_field.set.default("is_admin") is not True:
            raise ValueError("SuperUser must have is_admin=True")

        return self.create_user(username, email, password)

#creating custom user
class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(null=True, blank=true)

def __str__(self):
    return self.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"




