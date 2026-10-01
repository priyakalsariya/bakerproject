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

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','product')

    def __str__(self):
        return self.user.username

class Order(models.Model):
    PAYMENT_CHOICES=[
        ('cod','Cash on Delivery'),
        ('online','Online Payment'),
    ]

    STATUS_CHOICES=[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('processing','Processing'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)

    full_name=models.CharField(max_length=255,null=True,blank=True)

    phone=models.CharField(max_length=255,null=True,blank=True)

    address=models.TextField()

    city=models.CharField(max_length=100)

    state=models.CharField(max_length=100)

    pincode=models.CharField(max_length=100)

    payment_method=models.CharField(max_length=50,choices=PAYMENT_CHOICES,default="cod")

    total_amount=models.DecimalField(max_digits=10, decimal_places=2)

    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')

    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    quentity=models.PositiveIntegerField(default=1)

    price=models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quentity

    def __str__(self):
        return self.product.name