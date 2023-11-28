from django import forms
from django.forms import ValidationError

from admin_management.models import University,Address,Faculty
from django.contrib.auth.models import User


class  UniversityRegisterationForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ('university_name', 'email', 'mobile_number', 'address')

    def __init__(self, *args, **kwagrs):
        super(UniversityRegisterationForm, self).__init__(*args, **kwagrs)
        self.fields['address'].required = False



class  AddressRegisterationForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('address1', 'address2', 'city', 'zipcode', 'district',  'state', 'country')

    def __init__(self, *args, **kwagrs):
        super(AddressRegisterationForm, self).__init__(*args, **kwagrs)


class UserRegisterationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name',  'last_name', 'email', 'password')



class FacultyRegisterationForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ('phone_number',)

    def __init__(self, *args, **kwagrs):
        super(FacultyRegisterationForm, self).__init__(*args, **kwagrs)
        self.fields['address'].required = False
        self.fields['university'].required = False
        self.fields['username'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False



    

    
    





    