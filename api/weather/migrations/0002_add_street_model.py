# Generated by Django 2.0.3 on 2020-08-21 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial_model_changes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='street_name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='street_number',
        ),
        migrations.AddField(
            model_name='location',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='weather.Street'),
        ),
    ]
