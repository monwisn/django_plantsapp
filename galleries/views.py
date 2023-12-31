import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from galleries.models import Gallery, Photo, Status
from galleries.forms import GalleryForm, PhotoForm, GalleryPhotosFormset
from plants_app.config import pagination
from main.tasks import send_mail_task


@login_required(login_url='/authentication/login')
def add_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            if Gallery.objects.filter(title=instance.title).exists():
                messages.error(request, 'A gallery with this name already exists, please choose a different name.')
            else:
                instance.save()
                messages.success(request, 'Your gallery has been created successfully.')
        else:
            messages.error(request, f'Something went wrong!\n\n {form.errors}')
        return redirect('galleries:add_gallery')
    else:
        form = GalleryForm()
    return render(request, "galleries/add_gallery.html", {"form": form})


@login_required(login_url='/authentication/login')
def galleries_list(request):
    gallery = Gallery.objects.filter(author=request.user)
    # gallery = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED)
    # gallery = Gallery.objects.filter(status=Status.PUBLISHED).annotate(p_count=Count("photos")).filter(p_count__gt=0)
    pages = pagination(request, gallery, 5)
    return render(request, "galleries/list_galleries.html", {"gallery": pages, 'page_obj': pages})


@login_required(login_url='/authentication/login')
def galleries_list_view(request):
    galleries = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED).annotate(
        p_count=Count("photos")).filter(p_count__gt=0)
    # galleries = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED).annotate(
    #     p_count=Count("photos")).filter(p_count__gt=0)
    pages = pagination(request, galleries, 4)
    return render(request, 'galleries/galleries_list_view.html', {'galleries': pages, 'page_obj': pages})


@login_required(login_url='/authentication/login')
def gallery_details(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    count = gallery.photos.all()
    pages = pagination(request, count, 10)
    return render(request, "galleries/gallery_details.html", {"gallery": gallery, 'page_obj': pages})


@login_required(login_url='/authentication/login')
def gallery_edit(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk, author_id=request.user)
    if request.method == 'POST':
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery has been updated.')
            return redirect('galleries:list')
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'galleries/add_gallery.html', {'form': form, 'gallery': gallery})


@login_required(login_url='/authentication/login')
def gallery_delete(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'Gallery has been deleted.')
        return redirect('galleries:list')
    return render(request, 'galleries/gallery_delete.html', {'gallery': gallery})


@staff_member_required
def galleries_list_admin(request):
    galleries = Gallery.objects.all()
    pages = pagination(request, galleries, 15)
    return render(request, 'galleries/galleries_list_admin.html', {'galleries_list_admin': galleries,
                                                                   'page_obj': pages,
                                                                   })


@login_required(login_url='/authentication/login')
def add_photos(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    PhotosFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1)
    formset = PhotosFormSet(queryset=gallery.photos.none())
    form = PhotoForm()
    if request.method == "POST":
        formset = PhotosFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for f in formset.cleaned_data:
                if f:
                    Photo.objects.create(gallery=gallery, **f)
                    if f['send_reminder']:
                        if f['how_often'] == 'Once a week':
                            print('once a week')
                        elif f['how_often'] == 'Once every 2 weeks':
                            print('two weeks')
                        elif f['how_often'] == 'Once every 2-3 days':
                            print('2-3 days')
        messages.success(request, "Your photos have been successfully added to the gallery!")
        return HttpResponseRedirect(reverse("galleries:details", args=[gallery_id]))
    return render(request, "galleries/add_photos.html", {"formset": formset, "gallery": gallery, 'form': form})


@login_required(login_url='/authentication/login')
def photos_view(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    # photos = Photo.objects.filter(gallery__author=request.user)
    return render(request, "galleries/photos_view.html", {"gallery": gallery})


@login_required(login_url='/authentication/login')
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, f'Photo has been successfully deleted from "{photo.gallery.title}" gallery.')
        return redirect('galleries:list')
    return render(request, 'galleries/photo_delete.html', {'photo': photo})


class PhotosEditView(SingleObjectMixin, LoginRequiredMixin, FormView):
    model = Gallery
    template_name = 'galleries/photos_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Gallery.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Gallery.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return GalleryPhotosFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Photos have been successfully updated.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('galleries:details', kwargs={'gallery_id': self.object.pk})


@staff_member_required
def galleries_reminder(request):
    all_photos = Photo.objects.all().filter(send_reminder=True)
    for photo in all_photos:
        if photo.how_often == 'Once every 2-3 days':
            time = photo.updated + datetime.timedelta(days=3)
            print('1', time)
            send_mail_task.delay()
            print('sent')
        elif photo.how_often == 'Once a week':
            time = photo.updated + datetime.timedelta(weeks=1)
            print('2', time)
        elif photo.how_often == 'Once every 2 weeks':
            time = photo.updated + datetime.timedelta(weeks=2)
            print('3', time)
        else:
            print('4')

    # user = request.user
    # gal_users = Gallery.objects.all().values_list('author', flat=True).distinct()
    # if user.is_authenticated:
    #     # galleries = Gallery.objects.all().filter(author=user).filter(status=2)
    #     photos = Photo.objects.all().filter(gallery__author=user).filter(gallery__status=2).filter(send_reminder=True)
    #     for photo in photos:
    #         if photo.how_often == 'Once every 2-3 days':
    #             time = photo.updated + datetime.timedelta(days=3)
    #             print('1', time)
    #         elif photo.how_often == 'Once a week':
    #             time = photo.updated + datetime.timedelta(weeks=1)
    #             print('2', time)
    #         elif photo.how_often == 'Once every 2 weeks':
    #             time = photo.updated + datetime.timedelta(weeks=2)
    #             print('3', time)
    #         else:
    #             print('4')
    #
    #     return render(request, 'galleries/test-gallery.html', {'user': user,
    #                                                            # 'galleries': galleries,
    #                                                            'photos': photos,
    #                                                            'gal_users': gal_users})
    #
    # else:
    #     return redirect('authentication:login_user')

    return render(request, 'control_panel/control_send_reminder.html', {'all_photos': all_photos})
