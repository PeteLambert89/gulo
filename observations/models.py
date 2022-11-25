from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html

from observations import choices, constants


def format_user_as_string(user):
    if all([user.first_name, user.last_name, user.email]):
        return f'{user.first_name} {user.last_name} ({user.email})'
    else:
        return user.email


class Observation(models.Model):
    """ An observation of tracks at a place and time."""
    submission_date = models.DateTimeField(auto_now_add=True)
    observer_name = models.CharField(max_length=300)
    observer_email = models.EmailField(
        help_text='Please include the best email address to follow up with questions or '
        'information about the observation being submitted.'
    )
    date_of_observation = models.DateField()
    observation_type = models.CharField(
        'Footprints or Animal Observation',
        max_length = 2,
        choices = choices.ObservationTypes.choices,
    )
    location = models.CharField(
        max_length = 300, 
        null = True,
        help_text = 'Add a brief description of the general location the observation was made. If you '
        'didn\'t get a waypoint in the field but can pull one off of a map for us and include it here '
        'please do so (and note that in the notes section at the end of this form).'    
    )
    latitude = models.CharField(
        max_length = 300, 
        blank = True,
        null = True,  
        help_text = 'Enter as decimal degrees "00.000000"'
    )
    longditude = models.CharField(
        max_length = 300, 
        blank = True,
        null = True,  
        help_text = 'Enter as decimal degrees. Must be a negative number for our study zone. "-000.00000"'
    )
    elevation = models.IntegerField(
        blank = True,
        null = True,  
        help_text = 'Enter in feet'
    )
    observation_narrative = models.TextField(
        help_text='Record a short summary of the setting and details of the track or animal observation '
        'you are reporting'
    )

    def __str__(self):
        return f'Observation by "{self.observer_name}" on {self.date_of_observation}'

    def reviewed_by_user(self, user):
        if self.review_set.filter(reviewed_by=user).exists():
            colour = 'green'
            text = 'Yes'
        else:
            colour = 'orange'
            text = 'No'
        return format_html(f'<b style="color:{colour}">{text}</b>')

    @property
    def status(self):
        ''' The review status of the observation'''
        reviews = self.review_set.all()
        if reviews.count() < constants.MINIMUM_REVIEWS:
            text = 'Waiting for reviews'
            colour = 'black'
        elif all(review.suspected_species == reviews[0].suspected_species for review in reviews):
            text = f'Confirmed: {reviews[0].suspected_species}'
            colour = 'green'
        else:
            text = 'Inconclusive, discuss and find consensus'
            colour = 'orange'
        return format_html(f'<b style="color:{colour}">{text}</b>')

    @property
    def reviewers(self):
        return ', '.join(
            [format_user_as_string(review.reviewed_by) for review in self.review_set.all()]
        )

    @property
    def images(self):
        return self.trackimage_set.count()


class TrackImage(models.Model):
    """ Supporting images of tracks for each observation. """
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='track_images/%Y-%m-%d--%H-%M/')


class Species(models.Model):
    """ A species that could leave tracks."""
    common_name = models.CharField(max_length=300)
    latin_name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "species"

    def __str__(self):
        return f'{self.common_name} ({self.latin_name})'


class Review(models.Model):
    """ An expert assessment of an Observation."""
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    suspected_species = models.ForeignKey(Species, on_delete=models.CASCADE)
    notes = models.TextField()

    class Meta:
        unique_together = ['observation', 'reviewed_by']