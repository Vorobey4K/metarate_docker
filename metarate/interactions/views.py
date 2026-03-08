from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from catalog.models import MediaItem
from interactions.forms import ReviewForm
from interactions.models import UserMediaStatus, Review


# Create your views here.



def get_or_created_media_status(request):
    media_detail = MediaItem.objects.get(id=request.POST['media_id'])
    record = UserMediaStatus.objects.filter(user=request.user, mediaitem=media_detail)
    if not record:
        record = UserMediaStatus.objects.create(user=request.user, mediaitem=media_detail)
    else:
        record = record[0]
    return record

def planned(request):
    record = get_or_created_media_status(request)
    if record.status == record.Status.PLANNED:
        record.status = record.Status.NONE
    else:
        record.status = record.Status.PLANNED
    record.save()
    return HttpResponseRedirect(request.POST['next'])

def completed(request):
    record = get_or_created_media_status(request)
    if record.status == record.Status.COMPLETED:
        record.status = record.Status.NONE
    else:
        record.status = record.Status.COMPLETED
    record.save()
    return HttpResponseRedirect(request.POST['next'])

class ReviewCreateView(CreateView):
    form_class = ReviewForm
    model = Review
    template_name = 'universal_form.html'
    extra_context = {'title':"Добавить рецензию",'title_button':'Добавить'}

    def dispatch(self, request, *args, **kwargs):
        self.mediaitem = get_object_or_404(MediaItem,slug=kwargs['slug'])
        return super().dispatch(request,*args,**kwargs)


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.mediaitem = self.mediaitem
        return super().form_valid(form)

    def get_success_url(self):

        return self.mediaitem.get_absolute_url()
