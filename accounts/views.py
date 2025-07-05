from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import ScrapedItem
from accounts.utils.scraper import scrape_fbi_seeking_info  # updated import

from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max, Q

class DetectChangesView(View):
    def get(self, request):
        now = timezone.now()
        yesterday = now - timedelta(days=1)

        # Filter items updated or omitted in last 24h
        recent_items = ScrapedItem.objects.filter(timestamp__gte=yesterday)

        # If you have a boolean field like 'is_omitted', include that:
        # recent_items = ScrapedItem.objects.filter(
        #     Q(timestamp__gte=yesterday) | Q(is_omitted=True)
        # )

        # Group by 'name' and get max timestamp per name
        latest_per_name = recent_items.values('name').annotate(
            max_timestamp=Max('timestamp')
        )

        # Collect the latest updated item for each unique name
        unique_latest_items = []
        for entry in latest_per_name:
            item = ScrapedItem.objects.filter(
                name=entry['name'],
                timestamp=entry['max_timestamp']
            ).first()
            if item:
                unique_latest_items.append(item)

        html = render_to_string("accounts/partials/detect_changes_modal.html", {
            "new_items": unique_latest_items,
            "checked_at": now,
        })

        return HttpResponse(html)

class ScrapedItemsListView(View):
    def get(self, request):
        search = request.GET.get("search", "").strip()
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        show_duplicates = request.GET.get("show_duplicates", "on") == "on"
        page = int(request.GET.get("page", 1))
        page_size = 20

        qs = ScrapedItem.objects.all()

        if search:
            qs = qs.filter(name__icontains=search)

        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                qs = qs.filter(timestamp__date__gte=start_date_parsed)

        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                qs = qs.filter(timestamp__date__lte=end_date_parsed)

        qs = qs.order_by("-timestamp")

        if not show_duplicates:
            seen_names = set()
            unique_items = []
            for item in qs:
                if item.name not in seen_names:
                    seen_names.add(item.name)
                    unique_items.append(item)
            qs = unique_items  # This is now a list
        else:
            qs = list(qs)  # Convert queryset to list

        start = (page - 1) * page_size
        end = start + page_size
        paginated_items = qs[start:end]

        html = render_to_string(
            "accounts/partials/scraped_items_list.html",
            {"items": paginated_items, "page": page}
        )
        return HttpResponse(html)
class RunScraperView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            scrape_fbi_seeking_info()  # 🟢 Now synchronous
            messages.success(request, "✅ Scraping completed!")
        except Exception as e:
            messages.error(request, f"❌ Scraping failed: {str(e)}")
        return redirect("dashboard")
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

class LoginPageView(TemplateView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # or any default page
        return super().dispatch(request, *args, **kwargs)


class LoginFormView(View):
    template_name = 'accounts/login_form.html'

    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(csrf_exempt)  # HTMX might fail CSRF check if not handled
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return HttpResponse(
                '<div class="text-green-500">Login successful!</div>'
                '<script>window.location.href = "/"</script>'
            )
        return HttpResponse('<div class="text-red-500">Invalid credentials</div>')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
