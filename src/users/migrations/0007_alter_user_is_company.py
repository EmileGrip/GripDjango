# Generated by Django 3.2.12 on 2023-02-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_company',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
