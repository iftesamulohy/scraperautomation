from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from accounts.utils.scraper import scrape_fbi_seeking_info

class RunScraperView(View):
    def get(self, request):
        scrape_fbi_seeking_info()
        messages.success(request, "Scraping completed!")
        return redirect('dashboard')
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
