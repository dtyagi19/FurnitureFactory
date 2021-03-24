from django.urls import path

from . import apiviews

urlpatterns = [
    path('feet/', apiviews.feet_view, name='feet_view'),
    path('feet/<int:feet_id>/', apiviews.feet_detail_view,
         name='feet_detail_view'),
    path('leg/', apiviews.leg_view, name='leg_view'),
    path('leg/<int:leg_id>/', apiviews.leg_detail_view,
         name='leg_detail_view'),
    path('table/', apiviews.table_view, name='table_view'),
    path('table/<int:table_id>/', apiviews.table_detail_view,
         name='table_detail_view'),
]
