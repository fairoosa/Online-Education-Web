
from django.db import models

from django.contrib.auth.models import User



class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.IntegerField( null=True)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    is_verified=models.BooleanField()
    profile_image=models.ImageField(blank=True)
    created_at=models.DateField(null=True)
    qualification=models.CharField(max_length=50, null=True)

  
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




    


