import os

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
        help_text = 'Please include the best email address to follow up with questions or '
        'information about the observation being submitted.'
    )
    date_of_observation = models.DateField()
    observation_type = models.CharField(
        'Footprints or Animal Observation',
        max_length = 1,
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
        help_text ='Record a short summary of the setting and details of the track or animal observation '
        'you are reporting'
    )
    photo_permission = models.CharField(
        help_text = 'Do you grant Cascades Wolverine Project permission to share your images publicly on our website or '
        'social media? (Photo will be credited to the name submitted in this form unless you ask for something '
        'different in the notes above)',
        max_length = 1,
        choices = choices.PhotoReleaseChoices.choices,
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

    def edit_button(self):
        return format_html(f'<span class="button">Edit</span>')


class TrackImage(models.Model):
    """ Supporting files (images, videos, ...) of tracks for each observation. """
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    file = models.FileField(upload_to='track_images/%Y-%m-%d--%H-%M/')

    def view(self):
        extension = os.path.splitext(self.file.url)[1]
        if self.file:
            if extension in constants.VIEWABLE_EXTENSIONS:
                content = f"<img src='{self.file.url}' style='max-width:{constants.TRACK_IMAGE_DISPLAY_WIDTH}px' />"
            else:
                content = f"<button class='button'>Download</button>"
            return format_html(f"<a href='{self.file.url}' target='_blank'>{content}</a>")
        else:
            return "-"
    view.allow_tags = True


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
    track_identification_score = models.IntegerField(
        help_text = 'Category 1: Definitive Wolverine. Category 2: Likely Wolverine. '
        'Category 3: Identity unknown (possibly wolverine). Category 4: Not a wolverine. '
        'Refer to these guidelines for category descriptions: '
        'https://drive.google.com/file/d/1UKgzsZ59fBdTuXp5VNV0Z38Hpm-R5-AO/view?usp=sharing',
        choices = choices.TrackIdentificationScoreChoices.choices,
    )
    suspected_species = models.ForeignKey(
        Species, 
        on_delete=models.CASCADE,
        verbose_name = 'Suspected Species (If not a wolverine)',
    )

    notes = models.TextField()

    class Meta:
        unique_together = ['observation', 'reviewed_by']