# Generated by Django 4.0.4 on 2023-11-02 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_carousel_created_carousel_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='image',
            field=models.ImageField(upload_to='carousel_images/'),
        ),
    ]