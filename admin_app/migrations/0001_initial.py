# Generated by Django 3.1.7 on 2021-12-28 10:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=20)),
                ('admin_email', models.CharField(max_length=50)),
                ('admin_pass', models.CharField(max_length=200)),
                ('admin_phone', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_code', models.TextField()),
                ('item_title', models.CharField(max_length=150)),
                ('item_desp', models.CharField(max_length=25)),
                ('item_price', models.CharField(max_length=25)),
                ('item_condition', models.CharField(max_length=40)),
                ('item_location', models.TextField()),
                ('item_status', models.CharField(max_length=40)),
                ('item_add_date', models.DateField(default=datetime.date.today)),
                ('item_add_time', models.TimeField(auto_now_add=True)),
                ('item_user_contact', models.CharField(max_length=20)),
                ('fk_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.category')),
                ('fk_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.city')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('user_email', models.CharField(max_length=50)),
                ('user_pass', models.CharField(max_length=200)),
                ('user_phone', models.CharField(max_length=12)),
                ('user_mode', models.CharField(max_length=40)),
                ('user_reg_date', models.DateTimeField(default=datetime.datetime(2021, 12, 28, 15, 47, 47, 156786))),
            ],
        ),
        migrations.CreateModel(
            name='User_City',
            fields=[
                ('user_city_id', models.AutoField(primary_key=True, serialize=False)),
                ('fk_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.city')),
                ('fk_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.country')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Item_Images',
            fields=[
                ('item_img_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_img_name', models.ImageField(upload_to='Item_Image')),
                ('fk_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.user'),
        ),
        migrations.AddField(
            model_name='city',
            name='fk_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.country'),
        ),
        migrations.CreateModel(
            name='Account_status',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_status', models.CharField(max_length=40)),
                ('account_code', models.CharField(max_length=200)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.user')),
            ],
        ),
    ]
