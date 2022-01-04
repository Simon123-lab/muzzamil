from datetime import datetime, date
from django.db import models

# Create your models here.
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=20)
    admin_email = models.CharField(max_length=50)
    admin_pass  = models.CharField(max_length=200)
    admin_phone = models.CharField(max_length=12)

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    fk_country = models.ForeignKey(Country,on_delete=models.CASCADE)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=50)
    user_pass  = models.CharField(max_length=200)
    user_phone = models.CharField(max_length=12)
    user_mode = models.CharField(max_length=40)
    user_reg_date = models.DateTimeField(default=datetime.now())

class User_Images(models.Model):
    user_img_id = models.AutoField(primary_key=True)
    user_img_name = models.ImageField(upload_to="User_Image")
    fk_user = models.ForeignKey(User, on_delete= models.CASCADE)

class User_City(models.Model):
    user_city_id = models.AutoField(primary_key=True)
    fk_country = models.ForeignKey(Country,on_delete=models.CASCADE)
    fk_city = models.ForeignKey(City,on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Account_status(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_status = models.CharField(max_length=40)
    account_code = models.CharField(max_length=200)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_code = models.TextField()
    item_title = models.CharField(max_length=150)
    item_desp = models.CharField(max_length=25)
    item_price = models.CharField(max_length=25)
    item_condition = models.CharField(max_length=40)
    item_location = models.TextField()
    item_status = models.CharField(max_length=40)
    item_add_date = models.DateField(default=date.today)
    item_add_time = models.TimeField(auto_now_add=True, blank=True)
    item_user_contact = models.CharField(max_length=20)
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    fk_city= models.ForeignKey(City, on_delete=models.CASCADE)

class Item_Images(models.Model):
    item_img_id = models.AutoField(primary_key=True)
    item_img_name = models.ImageField(upload_to="Item_Image")
    fk_item = models.ForeignKey(Item, on_delete= models.CASCADE)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_body = models.TextField()
    comment_date = models.DateField(default=date.today)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Contact(models.Model):
    contact_id= models.AutoField(primary_key=True)
    contact_uname= models.CharField(max_length=40)
    contact_uemail= models.CharField(max_length=50)
    contact_umessage = models.TextField()
