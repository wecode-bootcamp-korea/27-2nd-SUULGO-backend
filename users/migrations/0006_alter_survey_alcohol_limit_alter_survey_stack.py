# Generated by Django 4.0 on 2021-12-22 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_survey_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='alcohol_limit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.alcohollimit'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.stack'),
        ),
    ]
