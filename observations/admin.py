from django.contrib import admin

from observations import forms, models


class TrackImageInline(admin.TabularInline):
    model = models.TrackImage
    extra = 3
    readonly_fields = ['view']


class ReviewInline(admin.TabularInline):
    model = models.Review
    extra = 0
    readonly_fields = ['reviewed_by']

    def get_formset(self, request, obj, **kwargs):
        form = forms.CustomAdminReviewForm
        form.observation = obj
        form.user = request.user
        kwargs['form'] = form
        return super().get_formset(request, obj, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(reviewed_by=request.user)


@admin.register(models.Observation)
class ObservationAdmin(admin.ModelAdmin):
    inlines = (TrackImageInline, ReviewInline)

    def get_list_display(self, request):
        def reviewed_by_me(observation):
            return observation.reviewed_by_user(request.user)

        return [
            'edit_button',
            'id', 
            'submission_date',
            'observer_name',
            'observer_email',
            'images',
            'status',
            'reviewers',
            reviewed_by_me,
        ]
        
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['status', 'reviewers']
        if not request.user.is_superuser:
            # Add other fields at start to mimic order for superusers
            readonly_fields = [field.name for field in models.Observation._meta.fields] + readonly_fields 
        return readonly_fields


admin.site.register(models.Species)