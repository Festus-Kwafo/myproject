# Generated by Django 3.2.8 on 2021-12-04 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20211204_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='featured_image/%Y/%m/%d/'),
        ),
    ]
