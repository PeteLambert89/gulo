from django.db import models


class ObservationTypes(models.TextChoices):
    TRACKS = 'T', 'Tracks'
    DIRECT = 'D', 'Direct observation of an animal'
    BOTH = 'B', 'Both'

