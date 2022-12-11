from django.db import models


class ObservationTypes(models.TextChoices):
    TRACKS = 'T', 'Tracks'
    DIRECT = 'D', 'Direct observation of an animal'
    BOTH = 'B', 'Both'


class PhotoReleaseChoices(models.TextChoices):
    YES = 'Y', 'Yes'
    NO = 'N', 'No'
    WITH_PRIOR_CONTACT = 'C', 'Please contact me before use'


class TrackIdentificationScoreChoices(models.IntegerChoices):
    ONE = 1, '1. Definitive Wolverine'
    TWO = 2, '2. Likely Wolverine'
    THREE = 3, '3. Identify Unknown'
    FOUR = 4, '4. Not a Wolverine'


DiagnosticFeaturesChoices = (
    (1, 'Size range is correct'),
    (2, 'Overall shape of individual tracks is correct'),
    (3, 'All details in clear print are correct for the morphology of a wolverine foot'),
    (4, 'Track pattern and size is diagnostic for only a wolverine'),
    (5, 'There are no features in individual tracks or trail that counter-indicate a wolverine')
)