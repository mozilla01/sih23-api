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
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class ConsumerAccount(models.Model):
    location = models.CharField(max_length=50)
    stock = models.IntegerField()


class RailwayAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    operator_name = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=50, null=True)
    pf_no = models.IntegerField(null=True)
    contact_no = models.IntegerField(null=True)
    org_contact_no = models.IntegerField(null=True)
    address = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=50, null=True)
    aadhaar = models.FileField(upload_to=upload_to, blank=True, null=True)
    id_proof = models.FileField(upload_to=upload_to, blank=True, null=True)


class CompanyAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    operator_name = models.CharField(max_length=50)
    emp_position = models.CharField(max_length=50)
    contact_no = models.IntegerField()
    org_contact_no = models.IntegerField()
    address = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=50)
    aadhaar = models.FileField(upload_to=upload_to, blank=True, null=True)
    corporation_proof = models.FileField(upload_to=upload_to, blank=True, null=True)
    allocated = models.BooleanField(default=False)
    stock = models.FloatField(null=True, blank=True)
    consumer = models.OneToOneField(ConsumerAccount, on_delete=models.SET_NULL, null=True, blank=True)


class Rake(models.Model):
    railway = models.ForeignKey(RailwayAccount, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    source = models.IntegerField(null=True, blank=True, default=None)
    destination = models.IntegerField(null=True, blank=True, default=None)
    distance = models.IntegerField()
    operator = models.CharField(max_length=50, null=True)