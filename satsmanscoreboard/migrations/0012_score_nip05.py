# Generated by Django 4.0.4 on 2023-05-11 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satsmanscoreboard', '0011_score_ln_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='nip05',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]