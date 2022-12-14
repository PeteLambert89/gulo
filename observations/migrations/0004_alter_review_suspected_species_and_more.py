# Generated by Django 4.1.3 on 2022-12-11 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0003_review_track_identification_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='suspected_species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='observations.species', verbose_name='Suspected Species (If not a wolverine)'),
        ),
        migrations.AlterField(
            model_name='review',
            name='track_identification_score',
            field=models.IntegerField(choices=[(1, '1. Definitive Wolverine'), (2, '2. Likely Wolverine'), (3, '3. Identify Unknown'), (4, '4. Not a Wolverine')], help_text='Category 1: Definitive Wolverine. Category 2: Likely Wolverine. Category 3: Identity unknown (possibly wolverine). Category 4: Not a wolverine. Refer to these guidelines for category descriptions: https://drive.google.com/file/d/1UKgzsZ59fBdTuXp5VNV0Z38Hpm-R5-AO/view?usp=sharing'),
        ),
    ]
