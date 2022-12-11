# Generated by Django 4.1.3 on 2022-12-11 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0002_remove_trackimage_image_observation_photo_permission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='track_identification_score',
            field=models.IntegerField(choices=[(1, 'Definitive Wolverine'), (2, 'Likely Wolverine'), (3, 'Identify Unknown'), (4, 'Not a Wolverine')], default=1, help_text='Category 1: Definitive Wolverine. Category 2: Likely Wolverine. Category 3: Identity unknown (possibly wolverine). Category 4: Not a wolverine. Refer to these guidelines for category descriptions: https://drive.google.com/file/d/1UKgzsZ59fBdTuXp5VNV0Z38Hpm-R5-AO/view?usp=sharing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='observation',
            name='photo_permission',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('C', 'Please contact me before use')], help_text='Do you grant Cascades Wolverine Project permission to share your images publicly on our website or social media? (Photo will be credited to the name submitted in this form unless you ask for something different in the notes above)', max_length=1),
        ),
        migrations.AlterField(
            model_name='review',
            name='suspected_species',
            field=models.ForeignKey(help_text='(If not a wolverine)', on_delete=django.db.models.deletion.CASCADE, to='observations.species'),
        ),
    ]