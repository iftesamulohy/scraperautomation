from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import ScrapedItem, Token
from accounts.utils.scraper import scrape_fbi_seeking_info  # updated import

from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max, Q
from django.utils.timezone import make_aware, is_naive, now as timezone_now
from django.utils.dateparse import parse_datetime
class DetectChangesView(View):
    def get(self, request):
        now = timezone_now()

        token1_id = request.GET.get("token1")
        token2_id = request.GET.get("token2")

        if token1_id and token2_id:
            try:
                token1 = Token.objects.get(pk=token1_id)
                token2 = Token.objects.get(pk=token2_id)
            except Token.DoesNotExist:
                return HttpResponse("Invalid tokens selected.", status=400)

            items1 = ScrapedItem.objects.filter(token=token1)
            items2 = ScrapedItem.objects.filter(token=token2)

            names1 = set(items1.values_list("name", flat=True))
            names2 = set(items2.values_list("name", flat=True))

            newly_added_names = names2 - names1
            omitted_names = names1 - names2

            newly_added_items = items2.filter(name__in=newly_added_names)
            omitted_items = items1.filter(name__in=omitted_names)

        else:
            # fallback to default datetime-based comparison
            start_str = request.GET.get('start')
            end_str = request.GET.get('end')

            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            start_time = parse_datetime(start_str) if start_str else today_start
            end_time = parse_datetime(end_str) if end_str else now

            if is_naive(start_time):
                start_time = make_aware(start_time)
            if is_naive(end_time):
                end_time = make_aware(end_time)

            duration = end_time - start_time
            prev_start = start_time - duration
            prev_end = start_time

            prev_items = ScrapedItem.objects.filter(timestamp__gte=prev_start, timestamp__lt=prev_end)
            current_items = ScrapedItem.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)

            prev_names = set(prev_items.values_list('name', flat=True))
            current_names = set(current_items.values_list('name', flat=True))

            newly_added_names = current_names - prev_names
            omitted_names = prev_names - current_names

            newly_added_items = current_items.filter(name__in=newly_added_names)
            omitted_items = prev_items.filter(name__in=omitted_names)

        html = render_to_string("accounts/partials/detect_changes_modal.html", {
            "newly_added_items": newly_added_items,
            "omitted_items": omitted_items,
            "tokens": Token.objects.order_by("-created_at")[:20],  # for dropdown
            "selected_token1": token1_id,
            "selected_token2": token2_id,
            "checked_at": now,
        }, request=request)

        return HttpResponse(html)
class ScrapedItemsListView(View):
    def get(self, request):
        search = request.GET.get("search", "").strip()
        token_id = request.GET.get("token")
        show_duplicates = request.GET.get("show_duplicates", "on") == "on"
        page = int(request.GET.get("page", 1))
        page_size = 20

        qs = ScrapedItem.objects.all()

        if token_id:
            qs = qs.filter(token__id=token_id)

        if search:
            qs = qs.filter(name__icontains=search)

        qs = qs.order_by("-timestamp")

        if not show_duplicates:
            seen_names = set()
            unique_items = []
            for item in qs:
                if item.name not in seen_names:
                    seen_names.add(item.name)
                    unique_items.append(item)
            qs = unique_items  # Now it's a list
        else:
            qs = list(qs)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tokens"] = Token.objects.order_by("-created_at")[:50]
        context["selected_token"] = self.request.GET.get("token", "")
        return context

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
