from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from .forms import CreateAlbumForm, UploadImageForm
from .models import Album, Image


class CreateAlbumView(LoginRequiredMixin, FormView):
    template_name = "user/create-album.html"
    form_class = CreateAlbumForm
    success_url = '/accounts/profile'

    def form_valid(self, form):
        album = Album(owner=self.request.user,
                      name=form.cleaned_data['name'],
                      is_public=form.cleaned_data['is_public'],
                      date_created=date.today())
        album.save()
        return super().form_valid(form)


class AlbumListForUserView(ListView):
    template_name = 'albums/list-albums.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        if user == self.request.user:
            # The requested albums belong to the logged in user
            # A user is allowed to see their own private albums
            album_list = Album.objects.filter(owner=user)
        else:
            # The requested albums do not belong to the active user
            # A user is not allowed to see others' private albums
            album_list = Album.objects.filter(owner=user).filter(is_public=True)
        return album_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context


class UploadImageView(LoginRequiredMixin, FormView):
    template_name = "user/upload-image.html"
    form_class = UploadImageForm
    success_url = '/accounts/profile'

    def get_form_kwargs(self):
        # We need the authenticated user to get the list of albums owned by the user
        kwargs = super(UploadImageView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        # Upload file
        upload_location = form.upload_image(self.request.FILES['file'])
        # Save image data to database
        image = Image(album=form.cleaned_data['album'],
                      title=form.cleaned_data['title'],
                      location=upload_location,
                      date_uploaded=date.today())
        image.save()
        return super().form_valid(form)
