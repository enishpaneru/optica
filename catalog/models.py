from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from db_file_storage.model_utils import delete_file, delete_file_if_needed
# Create your models here.
from django import template
register = template.Library()
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid
class Glass(models.Model):

    name = models.CharField(max_length=24)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    glass_pic = models.FileField(upload_to='catalog.imagepic/bytes/filename/mimetype', blank=True, null=True)
    detail = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    price = models.PositiveIntegerField(blank=True)
    booker = models.ManyToManyField(User,blank=True,through='booking')


    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'glass_pic')

        super(Glass, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Glass, self).delete(*args, **kwargs)
        delete_file(self, 'glass_pic')


    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('glass-detail', args=[str(self.id)])

class GlassInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular Glass.")
    glass = models.ForeignKey('Glass', null=True)
    imprint = models.CharField(max_length=200)








    class Meta:
        ordering = ["id"]
        permissions = (("can_mark_returned", "Set book as returned"),)



    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.glass.name)
class Brand(models.Model):

    name = models.CharField(max_length=100)
    detail = models.TextField(max_length=200,null=True)
    brand_pic = models.ImageField(upload_to='catalog.imagepic/bytes/filename/mimetype', blank=True, null=True)



    def get_absolute_url(self):

        return reverse('brand-detail', args=[str(self.id)])


    def __str__(self):

        return '%s' % (self.name)
class booking(models.Model):

    user = models.ForeignKey(User)
    glass = models.ForeignKey(Glass)
    booknovalue = models.PositiveIntegerField(blank=True)
    bookdate=models.DateField(null=True, blank=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.glass.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('bookno-detail', args=[str(self.id)])
class imagepic(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
class OrderDetail(models.Model):

    glass = models.ForeignKey('Glass', null=True)
    orderno=models.IntegerField()
    orderuser=models.ForeignKey('Order', null=True)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s' % (self.id)
class Order(models.Model):

    user = models.ForeignKey(User)
    orderdate=models.DateField(null=True, blank=True)
    active=models.BooleanField(default=True)
    amount=models.IntegerField()
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.id)
class UserDetail(models.Model):

    user = models.ForeignKey(User)
    location=models.TextField(null=True, blank=True)
    contact=models.TextField(null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.user)
