from django.db import models
import shortuuid, uuid
# Create your models here.

def generate_short_uuid():
    return shortuuid.uuid()[:10].upper()

class Category(models.Model):
    id =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(default=generate_short_uuid, editable=False, max_length=12)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_code = models.CharField(default=generate_short_uuid, editable=False, max_length=12)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.customer.first_name} {self.customer.last_name} (ID: {self.id})"

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"CartItem: {self.quantity} X {self.product.name} in Cart ID {self.cart.id}"
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_code = models.CharField(default=generate_short_uuid, editable=False, max_length=12)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders')
    created_at = models.DateTimeField(auto_now_add= True)
    
    status =models.CharField(
        max_length=20,
        default="Pending",
        choices=[
            ("Pending","Pending"),
            ("Processing","Processing"),
            ("Shipped","Shipped"),
            ("Delivered","Delivered"),
            ("Cancelled","Cancelled"),
        ],
    )
    
    def __str__(self):
        return f"Order for {self.customer.first_name} {self.customer.last_name} (ID: {self.id})"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"OrderItem: {self.quantity} x {self.product.name} (ID: {self.id})"



    
