from django.db import models
from solo.models import SingletonModel
from datetime import time
# Create your models here.
class ScrapedItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    image_file = models.ImageField(upload_to='scraped_images/',null=True,blank=True)
    details_link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

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