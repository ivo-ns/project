# Generated by Django 4.1.3 on 2022-12-22 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_alter_vinylpurchase_user_vinylpurchaseitem_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VinylPurchase',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='VinylPurchaseItem',
            new_name='OrderItem',
        ),
    ]