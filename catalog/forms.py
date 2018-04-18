from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Glass,Brand,UserDetail
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.contrib.auth.forms import UserCreationForm

class BookGlassForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.remain = kwargs.pop('remain')
        self.glass=Glass.objects.get(pk=self.pk)
        super(BookGlassForm, self).__init__(*args, **kwargs)

    Bookno = forms.IntegerField(help_text="Enter Value less than 10")



    def clean_Bookno(self):
        data = self.cleaned_data['Bookno']

        #Check date is not in past.





        # Remember to always return the cleaned data.
        return data
    def clean(self):
        bookno = self.cleaned_data.get("Bookno")
        if bookno > 10:
            raise ValidationError(_('Very High amount of booking'))
        if bookno < 1:
            raise ValidationError(_('Invalid amount of booking'))
        if bookno*self.glass.price > self.remain:
            raise ValidationError(_('Your booking amount has surpassed limits'))
        return self.cleaned_data
class BuyGlassForm(forms.Form):


    Buyno = forms.IntegerField(help_text="Enter Value less than 10")



    def clean(self):
        buyno = self.cleaned_data.get("Buyno")

        return self.cleaned_data
class AddGlassForm(forms.Form):

    name=forms.CharField()
    brand=forms.ModelChoiceField(queryset=Brand.objects.all())
    glass_pic=forms.ImageField()
    detail= forms.CharField()
    price = forms.IntegerField()




    def clean(self):
        name = self.cleaned_data.get("name")
        brand = self.cleaned_data.get("brand")
        detail = self.cleaned_data.get("detail")
        price = self.cleaned_data.get("price")
        glass_pic = self.cleaned_data.get("glass_pic")

        return self.cleaned_data
class AddBrandForm(forms.Form):

    name=forms.CharField()

    brand_pic=forms.ImageField()
    detail= forms.CharField()





    def clean(self):
        name = self.cleaned_data.get("name")

        detail = self.cleaned_data.get("detail")

        brand_pic = self.cleaned_data.get("brand_pic")

        return self.cleaned_data
class UserCreateForm(ModelForm):


    password2 = forms.CharField(widget=forms.PasswordInput(),help_text="Confirm Password")
    password = forms.CharField(widget=forms.PasswordInput(),help_text="Confirm Password")
    location = forms.CharField()
    def clean(self):

        cleaned_data=super(UserCreateForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')

        validators.validate_password(password=password,user=username)
        if email in User.objects.all().values_list('email', flat=True):
            raise forms.ValidationError("This email already exists")
        if password != password2:
            raise forms.ValidationError("The two password fields must match. Got it!!??")
        return cleaned_data
    def save(self):
         # create new user
        new_user=User.objects.create_user(username=self.cleaned_data['username'],
                                    first_name=self.cleaned_data['first_name'],
                                    last_name=self.cleaned_data['last_name'],
                                    password=self.cleaned_data['password'],
                                    email=self.cleaned_data['email'],
                                    is_superuser=self.cleaned_data['is_superuser'],
                                        )
        m1=UserDetail(user=new_user,location=self.cleaned_data.get('location'))
        m1.save()
        return new_user

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','is_superuser')
class UserinfoChangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(UserinfoChangeForm, self).__init__(*args, **kwargs)

    username=forms.CharField(max_length=191)
    first_name=forms.CharField(max_length=191)
    last_name=forms.CharField(max_length=191)
    location = forms.CharField()
    def clean(self):

        cleaned_data=super(UserinfoChangeForm, self).clean()
        username = cleaned_data.get('username')
        userlist=User.objects.exclude(username=self.user.username).values_list('username', flat=True)
        print (userlist)
        if username in userlist:
            raise ValidationError(_('Account with this username already exists'))

        return cleaned_data
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
