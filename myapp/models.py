from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=30,null=False)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    color = models.CharField(max_length=50)
    color_image = models.CharField(max_length=30,null=False)
    stock_quantity = models.IntegerField()
    date = models.DateField(auto_now=True)

class Members(AbstractUser):
    address = models.TextField()
    tel = models.CharField(max_length=15)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    order_status = models.CharField(max_length=50,default='待出貨')

    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.orderitem_set.all())


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateField(auto_now_add=True)

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
