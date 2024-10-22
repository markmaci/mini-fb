from django.db import models
from django.urls import reverse

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