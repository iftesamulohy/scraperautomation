from django.db import models
from solo.models import SingletonModel
from datetime import time
# Create your models here.
import uuid
from django.db import models
from django.utils import timezone
class Token(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        local_time = timezone.localtime(self.created_at)
        return f"Token created on {local_time.strftime('%B %d, %Y at %I:%M %p')} - {self.uid.hex[:6]}"
class ScrapedItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    image_file = models.ImageField(upload_to='scraped_images/',null=True,blank=True)
    details_link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    def __str__(self):
        return self.name
    

class ScraperSchedule(SingletonModel):
    INTERVAL_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    interval = models.CharField(
        max_length=10,
        choices=INTERVAL_CHOICES,
        default='daily'
    )
    run_time = models.TimeField(
        help_text="Time of day to run the task",
        default=time(0, 0)  # Default: midnight (00:00)
    )

    def __str__(self):
        return "Scraper Schedule Settings"