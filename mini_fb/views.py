from django.shortcuts import redirect, render

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, UpdateView
from django.urls import reverse
from .models import Image, Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        status_message = form.save(commit=False)
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        status_message.profile = profile
        status_message.save()

        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(status_message=status_message, image_file=f)
        
        return redirect(status_message.get_absolute_url())

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.kwargs.get('pk')])
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.pk])

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.profile.pk])
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm  # Reuse the form for creating status
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.profile.pk])

