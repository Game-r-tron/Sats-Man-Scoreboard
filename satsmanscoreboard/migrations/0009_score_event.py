# Generated by Django 4.0.4 on 2022-06-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satsmanscoreboard', '0008_alter_score_score_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='event',
            field=models.CharField(default='none', max_length=20),
            preserve_default=False,
        ),
    ]