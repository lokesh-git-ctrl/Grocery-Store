# Generated by Django 5.1.4 on 2024-12-21 07:39

import Shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0009_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='path/to/default/image.jpg', null=True, upload_to=Shop.models.getFileName),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=False, help_text='0-show, 1-Hidden'),
        ),
    ]
