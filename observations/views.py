from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import base, edit

from observations import forms, formsets, models, permissions


class CreateFormSetMixin:
    """ A mixin for adding and processing formsets in CreateViews
    The inheriting view must set:
        self.formset_class (FormSetObject)
        self.formset_prefix (To be referenced in template) """
    formset_prefix = 'formset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.POST:
            context[self.formset_prefix] = self.formset_class(prefix=self.formset_prefix)
        return context

    def form_valid(self, form):
        # Associate and save formset
        formset = self.formset_class(
            self.request.POST, 
            self.request.FILES, 
            prefix=self.formset_prefix,
        )
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            super().form_valid(formset)
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        ''' Allows for redirect without errors.'''
        if self.success_url:
            return self.success_url
        else:
            return super().get_success_url(self)


class ObservationSubmission(CreateFormSetMixin, edit.CreateView):
    model = models.Observation
    template_name = 'observations/observation_submission.html'
    form_class = forms.ObservationForm
    formset_class = formsets.ObservationImageFormSet
    formset_prefix = 'image_formset'
    success_url = reverse_lazy('observation-submission-acknowledgement')


class ObservationSubmissionAcknowledgement(base.TemplateView):
    template_name = 'observations/observation_submission_acknowledgement.html'


class CreateReviewer(edit.CreateView):
    model = User
    fields = [
        'email',
        'first_name',
        'last_name',
        'password',
    ]
    template_name = 'observations/create_user.html'
    success_url = reverse_lazy('admin:index')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        print(dir(form.fields['email']))
        form.fields['email'].required = True
        form.fields['first_name'].required = True
        form.fields['last_name'].required = True
        return form

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.username = form.instance.email
            form.instance.set_password(form.instance.password)
            form.instance.is_staff = True
            response = super().form_valid(form)
            print(dir(response))
            form.instance.user_permissions.set(permissions.default_reviewer_permission_queryset)
            print('obj: ', self.object)
            return response


class CreateManager(CreateReviewer):
    for_manager = True # For template

    def form_valid(self, form):
        form.instance.is_superuser = True
        return super().form_valid(form)