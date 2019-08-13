from django.db import models

# Create your models here.


class Org(models.Model):
    company = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Org_login(models.Model):
    company = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Services(models.Model):
    company = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=2, default='P')


class Admin(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class Admin_login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=200)

class Question(models.Model):
	Category_id = models.CharField(max_length=200)
	Question = models.TextField(max_length = 500)

class Review(models.Model):
    Category_id = models.CharField(max_length=200)
    review1 = models.CharField(max_length=100)
    review2 = models.CharField(max_length=100)
    review3 = models.CharField(max_length=100)
    review4 = models.CharField(max_length=100)
    review5 = models.CharField(max_length=100)
    comment = models.TextField(max_length=500)
