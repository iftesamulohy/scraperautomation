from django.db import models
from solo.models import SingletonModel
# Create your models here.
class ScrapedItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
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

    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES, default='daily')
    run_time = models.TimeField(help_text="Time of day to run the task")

    def __str__(self):
        return "Scraper Schedule Settings"