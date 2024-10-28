from django.db import models
from django.urls import reverse
from django.db.models import Q

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('mini_fb:show_profile', args=[str(self.pk)])

    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        friends = [friend.profile2 for friend in friends_as_profile1] + \
                  [friend.profile1 for friend in friends_as_profile2]
        
        return friends

    def add_friend(self, other):
        if self == other:
            return False
        
        friendship_exists = Friend.objects.filter(
            Q(profile1=self, profile2=other) | 
            Q(profile1=other, profile2=self)
        ).exists()
        
        if friendship_exists:
            return False
        
        Friend.objects.create(profile1=self, profile2=other)
        return True

    def get_news_feed(self):
        friends = self.get_friends()
        
        profiles = friends + [self]
        
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        
        return news_feed

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name='friend_profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='friend_profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"

    class Meta:
        unique_together = ('profile1', 'profile2')

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='status_images/', blank=True)

    def __str__(self):
        return f"StatusMessage by {self.profile.first_name} {self.profile.last_name} at {self.timestamp}: {self.message[:20]}..."

    def get_absolute_url(self):
        return reverse('mini_fb:show_profile', kwargs={'pk': self.profile.pk})

    def get_images(self):
        return self.images.all()

class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='status_images/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.pk} uploaded at {self.timestamp}"