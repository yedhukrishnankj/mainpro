from django.db import models
from django.contrib.auth.models import User
from textblob import TextBlob

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=30, null=True,unique=True)

    def __str__(self):
        return self.city

class Status(models.Model):
    status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.status


class ID_Card(models.Model):
    card = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.card


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.first_name


class Service_Man(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    doj = models.DateField(null=True)
    dob = models.DateField(null=True)
    id_type = models.CharField(max_length=100, null=True)
    service_name = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    id_card = models.FileField(null=True)
    image = models.FileField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


    def __str__(self):
        return self.user.first_name
    
    def get_overall_rating(self):
        ratings = Rating.objects.filter(service_man=self)
        total_ratings = sum(r.rating for r in ratings)
        if ratings:
            return round(total_ratings / len(ratings), 1)
        else:
            return 0.0


class Service_Category(models.Model):
    category = models.CharField(max_length=30, null=True)
    desc = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    total = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category


class Service(models.Model):
    category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service_Man, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service.user.first_name


class Contact(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    message1 = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    sentiment_score = models.FloatField(null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.message1:
            blob = TextBlob(self.message1)
            self.sentiment_score = blob.sentiment.polarity
        else:
            self.sentiment_score = None
        super(Contact, self).save(*args, **kwargs)


class Total_Man(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service.user.first_name


class Order(models.Model):
    report_status = models.CharField(max_length=100, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service_Man, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    book_date = models.DateField(null=True)
    book_days = models.CharField(max_length=100, null=True)
    book_hours = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.service.user.first_name + " " + self.customer.user.first_name


class place(models.Model):
    name = models.CharField(max_length=250,unique=True,null=True)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField(null=True)

    def __str__(self):
        return self.home_place

class Rating(models.Model):
    service_man = models.ForeignKey(Service_Man, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.service_man.user.first_name + " - " + self.customer.user.first_name
    
class Feedback(models.Model):
    service_man = models.ForeignKey(Service_Man, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feedback_text = models.TextField()

    def __str__(self):
        return self.service_man.user.first_name + " - " + self.customer.user.first_name