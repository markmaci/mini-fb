from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

# Create your views here.

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, UpdateView
from django.urls import reverse
from .models import Image, Profile, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_profiles'] = Profile.objects.exclude(pk=self.object.pk)
        return context

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
    
class CreateFriendView(View):
    def get(self, request, pk, other_pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        friendship_created = profile.add_friend(other_profile)
        
        if friendship_created:
            messages.success(request, f"You are now friends with {other_profile.first_name} {other_profile.last_name}!")
        else:
            messages.error(request, "Cannot add this friend. They may already be your friend or you cannot add yourself.")
        
        return redirect('mini_fb:show_profile', pk=pk)
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['news_feed'] = profile.get_news_feed()
        return context