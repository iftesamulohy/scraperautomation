from django.urls import path
from .views import LoginPageView, LoginFormView, LogoutView,DashboardView,RunScraperView,ScrapedItemsListView,DetectChangesView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('login-form/', LoginFormView.as_view(), name='login_form'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('run-scraper/', RunScraperView.as_view(), name='run_scraper'),
    path('scraped-items-list/', ScrapedItemsListView.as_view(), name='scraped_items_list'),
    path("detect-changes/", DetectChangesView.as_view(), name="detect_changes"),
]
