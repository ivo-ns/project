# Generated by Django 4.1.3 on 2022-12-13 10:19

from django.db import migrations, models
import django.db.models.deletion
import final_project.web.validators


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_artist_name_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.style'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(validators=[final_project.web.validators.age_validator]),
        ),
    ]