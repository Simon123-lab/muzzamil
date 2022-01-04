# Generated by Django 4.0 on 2021-12-29 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_auto_20211228_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_uname', models.CharField(max_length=40)),
                ('contact_uemail', models.CharField(max_length=50)),
                ('contact_umessage', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='user_reg_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 29, 22, 20, 49, 686670)),
        ),
    ]