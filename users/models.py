from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, DateField, EmailField, OneToOneField, CASCADE, IntegerField, DateTimeField
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    SEX_CHOICES = (
        ('F', "Female"),
        ('M', 'Male'),
    )
    sex = CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = DateField(null=True, blank=True)
    email = EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class ConnectedUsers(Model):
    user = OneToOneField(get_user_model(), on_delete=CASCADE)
    count = IntegerField(default=1)
    last_joined = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
