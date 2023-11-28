from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Address(models.Model):
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField( max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    zipcode = models.IntegerField( null=True)
    district = models.CharField( max_length=50, null=True)
    state = models.CharField( max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.address1}-{self.city}'


class University(models.Model):
    university_name = models.CharField(max_length=100, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    email = models.EmailField()
    mobile_number = models.IntegerField(max_length=15)


    def __str__(self):
        return self.university_name


class Faculty(models.Model): 
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone_number=models.IntegerField( null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.first_name





