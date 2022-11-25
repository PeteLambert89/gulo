from django import forms
from django.core.exceptions import ValidationError

from observations import models


class ObservationForm(forms.ModelForm):
    ''' Main form for frontend submissions.'''
    class Meta:
        model = models.Observation
        fields = '__all__'
        labels = {
            "observer_name": "Your name",
            "observer_email": "Your email",
        }


class CustomAdminReviewForm(forms.ModelForm):
    ''' Form.observation and .user attribute must be dynamically before use, to populate new forms.'''
    class Meta:
        model = models.Review
        fields = '__all__'

    def clean(self):
        ''' Enforces user-level uniqueness.'''
        cleaned_data = super().clean()
        if not cleaned_data.get('reviewed_by'):
            if self.instance.pk is None and models.Review.objects.filter( # Check if adding and exists
                observation = self.observation,
                reviewed_by = self.user
            ).exists():
                raise ValidationError('You\'ve already reviewed this Observation!')
        return cleaned_data

    def save(self, commit):
        ''' Adds user as reviewed_by when not present.'''
        if self.instance.pk:
            return super().save(commit)
        else:
            review = super().save(False)
            review.reviewed_by = self.user
            review.save(commit)
            return review