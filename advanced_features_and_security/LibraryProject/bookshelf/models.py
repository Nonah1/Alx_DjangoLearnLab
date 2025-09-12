from django.db import models Group, Permission
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.contrib.auth.models import 

content_type = ContentType.objects.get_for_model(Book)

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

    class Meta:
        permissions =[
            ("can_view", "Can view Book")
            ("can_create", "Can create Book")
            ("can_edit", "Can edit Book")
            ("can_delete", "Can delete Book")
]

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

#define permission
view_permission = Permission.objects.get(codename="can_view", content_type=content_type)
create_permission = Permission.objects.get(codename="can_create", content_type=cpntent_type)
edit_permission = Permission.objects.get(codename="can_edit", content_type=content_type)
delete_permission = Permission.objects.get(codename="can_delete", content_type=content_type)

#create groups
viewers.permissions.set([view_permissions])
editors.permissions.set([edit_permissions, create_permission])
editors.permissions.set([edit_permissions, create_permission, edit_permissions, delete_permission])

