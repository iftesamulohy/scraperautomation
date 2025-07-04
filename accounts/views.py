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
class ScrapedItemsListView(View):
    def get(self, request):
        # Get query params from htmx request
        search = request.GET.get("search", "").strip()
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        show_duplicates = request.GET.get("show_duplicates") == "on"

        qs = ScrapedItem.objects.all()

        if search:
            qs = qs.filter(name__icontains=search)

        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                qs = qs.filter(scraped_at__date__gte=start_date_parsed)

        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                qs = qs.filter(scraped_at__date__lte=end_date_parsed)

        if not show_duplicates:
            # show only one record per unique (name, details_link, image)
            qs = qs.distinct("name", "details_link", "image")

        qs = qs.order_by("-scraped_at")[:50]  # limit to last 50 for performance

        html = render_to_string("partials/scraped_items_list.html", {"items": qs})
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
