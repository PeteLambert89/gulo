from django.urls import path

from observations import views


urlpatterns = [
    path('', views.ObservationSubmission.as_view(), name='observation-submission'),
    path('thanks/', views.ObservationSubmissionAcknowledgement.as_view(), name='observation-submission-acknowledgement'),
    path('new-reviewer', views.CreateReviewer.as_view(), name='new-reviewer'),
    path('new-manager', views.CreateManager.as_view(), name='new-manager'),
]
