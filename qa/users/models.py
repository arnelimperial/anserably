from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from qa.users.managers import UserManager

class User(AbstractUser):
    first_name = CharField(_("First Name"), max_length=100)
    last_name = CharField(_("Last Name"), max_length=100)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

