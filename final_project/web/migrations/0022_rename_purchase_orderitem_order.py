# Generated by Django 4.1.3 on 2022-12-22 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_rename_vinylpurchase_order_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='purchase',
            new_name='order',
        ),
    ]
