# Generated by Django 4.0 on 2021-12-15 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='alcohol_level',
            field=models.CharField(max_length=100),
        ),
    ]