from django.urls import path

from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:id>/', api.post_detail, name='post_detail'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('profile/<uuid:id>/received/', api.post_list_profile_received, name='post_list_profile_received'),
    path('profile/<uuid:id>/saved/', api.post_list_profile_saved, name='post_list_profile_saved'),
    path('create/', api.post_create, name='post_create'),
    path('<uuid:id>/like/', api.post_like, name='post_like'),
    path('<uuid:id>/save/', api.post_save, name='post_save'),
    path('<uuid:id>/edit/', api.post_edit, name='post_edit'),
    path('<uuid:id>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:id>/report/', api.post_report, name='post_report'),
    path('<uuid:id>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:id>/comment/<uuid:pk>/delete/', api.post_delete_comment, name='post_delete_comment'),
    path('<uuid:id>/comment/report/', api.post_report_comment, name='post_report_comment'),
    path('trends/', api.get_trends, name='get_trends'),
    path('mediatypes/', api.get_media_types, name='get_media_types'),
    path('genres/', api.get_genres, name='get_genres'),
]
