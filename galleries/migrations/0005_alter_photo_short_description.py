# Generated by Django 4.0.4 on 2022-12-06 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='short_description',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
