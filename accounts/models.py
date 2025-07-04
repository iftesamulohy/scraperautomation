from django.db import models

# Create your models here.
class ScrapedItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    details_link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name