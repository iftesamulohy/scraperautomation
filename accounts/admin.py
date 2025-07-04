from django.contrib import admin

from accounts.models import ScrapedItem

# Register your models here.
@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'details_link', 'timestamp')
    search_fields = ('name',)
    ordering = ('-timestamp',)