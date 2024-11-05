from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_profiles'] = Profile.objects.exclude(pk=self.object.pk)
        return context

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['user_form'] = UserCreationForm()
        else:
            context['user_form'] = UserCreationForm(self.request.POST)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST)
        user_form = UserCreationForm(self.request.POST)

        if form.is_valid() and user_form.is_valid():
            return self.form_valid(form, user_form)
        else:
            return self.form_invalid(form, user_form)

    def form_valid(self, form, user_form):
        user = user_form.save()
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        login(self.request, user)
        return redirect('mini_fb:show_profile', pk=profile.pk)

    def form_invalid(self, form, user_form):
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form))


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            messages.error(request, "You can only update your own profile.")
            return redirect('mini_fb:show_profile', pk=self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.pk])

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        status_message = form.save(commit=False)
        status_message.profile = self.request.user.profile
        status_message.save()

        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(status_message=status_message, image_file=f)

        return redirect(status_message.get_absolute_url())

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.request.user.profile.pk])

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status'

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        if status_message.profile.user != request.user:
            messages.error(request, "You can only update your own status messages.")
            return redirect('mini_fb:show_profile', pk=status_message.profile.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.profile.pk])

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        if status_message.profile.user != request.user:
            messages.error(request, "You can only delete your own status messages.")
            return redirect('mini_fb:show_profile', pk=status_message.profile.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mini_fb:show_profile', args=[self.object.profile.pk])

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['news_feed'] = profile.get_news_feed()
        return context

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        suggestions = profile.get_friend_suggestions()
        context['suggestions'] = suggestions
        return context

class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, other_pk):
        profile = request.user.profile
        other_profile = get_object_or_404(Profile, pk=other_pk)

        if profile.add_friend(other_profile):
            messages.success(request, f"You are now friends with {other_profile.first_name} {other_profile.last_name}!")
        else:
            messages.info(request, "Cannot add this friend.")

        return redirect('mini_fb:friend_suggestions')
