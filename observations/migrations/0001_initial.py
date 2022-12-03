# Generated by Django 4.1.3 on 2022-11-25 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('observer_name', models.CharField(max_length=300)),
                ('observer_email', models.EmailField(help_text='Please include the best email address to follow up with questions or information about the observation being submitted.', max_length=254)),
                ('date_of_observation', models.DateField()),
                ('observation_type', models.CharField(choices=[('T', 'Tracks'), ('D', 'Direct observation of an animal'), ('B', 'Both')], max_length=2, verbose_name='Footprints or Animal Observation')),
                ('location', models.CharField(help_text="Add a brief description of the general location the observation was made. If you didn't get a waypoint in the field but can pull one off of a map for us and include it here please do so (and note that in the notes section at the end of this form).", max_length=300, null=True)),
                ('latitude', models.CharField(blank=True, help_text='Enter as decimal degrees "00.000000"', max_length=300, null=True)),
                ('longditude', models.CharField(blank=True, help_text='Enter as decimal degrees. Must be a negative number for our study zone. "-000.00000"', max_length=300, null=True)),
                ('elevation', models.IntegerField(blank=True, help_text='Enter in feet', null=True)),
                ('observation_narrative', models.TextField(help_text='Record a short summary of the setting and details of the track or animal observation you are reporting')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=300)),
                ('latin_name', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'species',
            },
        ),
        migrations.CreateModel(
            name='TrackImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='track_images/%Y-%m-%d--%H-%M/')),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.observation')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField()),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.observation')),
                ('reviewed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('suspected_species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observations.species')),
            ],
            options={
                'unique_together': {('observation', 'reviewed_by')},
            },
        ),
    ]