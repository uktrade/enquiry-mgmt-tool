from django.urls import path

from app.testfixtureapi import views


app_name = 'testfixtureapi'
urlpatterns = [
    path('reset-fixtures/', views.ResetFixturesView.as_view(), name='reset-fixtures'),
]
