from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=254,blank=True,null=True)
    subject=models.CharField(max_length=255,null=True,blank=True)
    message=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey("Category",on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.BigIntegerField(default=0)
    image=models.ImageField(upload_to='products',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username 

class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items') 
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.products.name} - {self.quentity}'

    @property
    def total_price(self):
        return self.products.price * self.quentity

