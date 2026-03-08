from django.urls import path

from interactions.views import planned,completed, ReviewCreateView

app_name ='interactions'

urlpatterns = [
    path('planned/',planned,name='planned'),
    path('completed/',completed,name='completed'),
    path('review_create/<slug:slug>',ReviewCreateView.as_view(),name='review_create')
   ]
