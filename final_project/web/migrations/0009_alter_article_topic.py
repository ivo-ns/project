# Generated by Django 4.1.3 on 2022-12-18 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_vinyl_artist_vinyl_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.style'),
        ),
    ]
