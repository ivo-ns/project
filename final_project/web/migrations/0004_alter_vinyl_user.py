# Generated by Django 4.1.3 on 2022-12-13 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_artist_style_alter_profile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinyl',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
