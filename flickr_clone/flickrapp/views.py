from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from .forms import CreateAlbumForm
from .models import Album


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
