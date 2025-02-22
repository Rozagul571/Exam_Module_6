from datetime import timezone, timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models import CharField, EmailField, BooleanField, IntegerField, DateField, DateTimeField, DecimalField, \
    TextChoices, Model, ImageField, PositiveIntegerField, ForeignKey, ManyToManyField, TextField


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser uchun is_staff=True bo'lishi kerak")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser uchun is_superuser=True bo'lishi kerak")
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    # avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    email = EmailField("Email address", unique=True)
    is_active = BooleanField(default=False)
    job = CharField(max_length=255)
    date = DateField(blank=True, null=True)
    country = CharField(max_length=255)
    phone = IntegerField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Transaction(Model):
    class STATUS_CHOICES(TextChoices):
        Completed = 'completed', 'Completed',
        Pending = 'pending', 'Pending',
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=20, unique=True)
    date = DateField()
    name = CharField(max_length=255)
    amount = DecimalField(max_digits=10, decimal_places=2)
    is_income = BooleanField(default=False)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    image = ImageField(upload_to='products/', blank=True, null=True)
    stock = PositiveIntegerField(default=0)  # Mahsulot ombordagi soni

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = ForeignKey(Product, on_delete=models.CASCADE)
    quantity = PositiveIntegerField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = ManyToManyField(CartItem)
    created_at = DateTimeField(auto_now_add=True)
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    special_note = TextField(blank=True, null=True)
