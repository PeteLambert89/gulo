# Generated by Django 4.1.3 on 2022-12-11 05:14

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0005_review_diagnostic_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='diagnostic_features',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Size range is correct'), (2, 'Overall shape of individual tracks is correct'), (3, 'All details in clear print are correct for the morphology of a wolverine foot'), (4, 'Track pattern and size is diagnostic for only a wolverine'), (5, 'There are no features in individual tracks or trail that counter-indicate a wolverine')], help_text='If tracks are "1. Definitive Wolverine" what did you observe?', max_length=10),
        ),
        migrations.AlterField(
            model_name='review',
            name='suspected_species',
            field=models.ForeignKey(blank=True, help_text='If not a wolverine', null=True, on_delete=django.db.models.deletion.CASCADE, to='observations.species'),
        ),
    ]
