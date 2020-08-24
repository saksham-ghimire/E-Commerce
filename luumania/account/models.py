from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

class SignUp(models.Model):

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    E_mail = models.EmailField(max_length=200)
    comfirm = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Address_url = models.URLField(max_length=200, null=True, blank=True)
    E_sewa = models.CharField(max_length=200)
    Phone_number = models.CharField(max_length=10)
    Service=models.CharField(max_length=5, blank=True, null=True)

    Shopkeeper=models.CharField(max_length=5, blank=True, null=True)




class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = (
    ('shop', 'Shopkeeper'),
    ('blog', 'Blogger'),
    )
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, null=True, blank=True, default=None)
    username=models.CharField(max_length=200)
    Image1=models.ImageField(default=None, upload_to="images", blank=True, null=True)
    Phone_number = models.CharField(max_length=10)
    Address = models.CharField(max_length=200)
    Address_url = models.URLField(max_length=200, null=True, blank=True)
    Service=models.CharField(max_length=5, blank=True, null=True)
    First_name=models.CharField( default=None, blank=True, null=True, max_length=200)
    Last_name=models.CharField(default=None, blank=True, null=True, max_length=200)
    Contact=models.CharField( default=None, blank=True, null=True, max_length=200)
    Address_per=models.CharField( default=None, blank=True, null=True, max_length=200)
    Facebook=models.CharField( default=None, blank=True, null=True, max_length=200)
    Instagram=models.CharField( default=None, blank=True, null=True, max_length=200)
    CITY_CHOICES = (('Kathmandu','Kathmandu'),
                    ('Pokhara','Pokhara'),
                    ('Biratnagar', 'Biratnagar'),
                    ('Bhaktapur','Bhaktapur'),
                    ('Lalitpur','Lalitpur'),
                    ('Nepalgunj','Nepalgunj'))
    City=models.CharField( default=None, blank=True, choices=CITY_CHOICES, null=True, max_length=200)
