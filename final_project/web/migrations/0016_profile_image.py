# Generated by Django 4.1.3 on 2022-12-22 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_alter_profile_first_name_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/images/default_profile_pic.png', upload_to='profiles/'),
        ),
    ]
