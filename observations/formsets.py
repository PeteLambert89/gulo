from django.forms import inlineformset_factory

from observations import models


ObservationImageFormSet = inlineformset_factory(
    models.Observation,
    models.TrackImage,
    fields = '__all__',
    extra = 10,
    can_delete = False
)