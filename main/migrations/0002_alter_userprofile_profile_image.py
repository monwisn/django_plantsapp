# Generated by Django 4.0.4 on 2022-10-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='profile/default_user.jpg', upload_to='profile_pictures'),
        ),
    ]