# Generated by Django 4.0.4 on 2022-06-23 17:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('satsmanscoreboard', '0004_alter_score_score_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.AddField(
            model_name='score',
            name='expiresAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='score',
            name='zbdId',
            field=models.CharField(default=3234, max_length=50),
            preserve_default=False,
        ),
    ]
