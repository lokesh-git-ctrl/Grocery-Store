# Generated by Django 5.1.4 on 2024-12-19 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_remove_product_status_remove_product_trending'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catagory',
            new_name='Category',
        ),
    ]
