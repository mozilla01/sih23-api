from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


def upload_to(instance, filename):
    return "documents/{filename}".format(filename=filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    type = models.CharField(max_length=10, null=True)
    operator_name = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=50, null=True)
    emp_position = models.CharField(max_length=50, null=True)
    pf_no = models.IntegerField(null=True)
    contact_no = models.IntegerField(null=True)
    org_contact_no = models.IntegerField(null=True)
    address = models.TextField(max_length=500, null=True)
    aadhaar = models.FileField(upload_to=upload_to, blank=True, null=True)
    id_proof = models.FileField(upload_to=upload_to, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
