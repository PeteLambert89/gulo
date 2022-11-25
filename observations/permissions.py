from django.contrib.auth.models import Permission


DEFAULT_REVIEWER_PERMISSIONS = [
    'view_observation',
    'change_observation',
    'view_review',
    'add_review',
    'change_review',
    'delete_review',
    'view_species',
    'add_species',
    'change_species',
    'view_trackimage',
]

default_reviewer_permission_queryset = Permission.objects.filter(codename__in=DEFAULT_REVIEWER_PERMISSIONS)