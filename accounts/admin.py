from django.contrib import admin

from accounts.models import ScrapedItem, ScraperSchedule
from solo.admin import SingletonModelAdmin

# Register your models here.
@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'details_link', 'timestamp')
    search_fields = ('name',)
    ordering = ('-timestamp',)
admin.site.register(ScraperSchedule, SingletonModelAdmin)