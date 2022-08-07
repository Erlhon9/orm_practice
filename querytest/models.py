from datetime import datetime
from django.db import models

"""
product <- product attr <- stock  <-
stockbox                          <- stockboxitem
"""

class Product(models.Model):
    name: str = models.CharField(max_length=100, null=False)
    price: int = models.PositiveIntegerField(null=False)

    
class ProductAttr(models.Model):
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sizes: str = models.CharField(max_length=100, null=False)
    style: str = models.CharField(max_length=100, null=False)

    
class Stock(models.Model):
    product_attr: ProductAttr = models.ForeignKey(ProductAttr, on_delete=models.CASCADE)
    code: str = models.CharField(max_length=100, null=False)

    
class StockBox(models.Model):
    address: str = models.CharField(max_length=100, null=False)
    created_time: datetime = models.DateTimeField(auto_created=True)
    

class StockBoxItem(models.Model):
    stock: Stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock_box: StockBox = models.ForeignKey(StockBox, on_delete=models.CASCADE)
    
    
## 추후 many to many, one to one 도 포함하기