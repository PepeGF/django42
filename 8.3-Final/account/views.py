from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


class AccountView(TemplateView):
    template_name = "account/index.html"


class LoginAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse(
                {
                "success": True,
                "username": user.username,
            })
        errors = {field: [str(error) for error in field_errors] for field, field_errors in form.errors.items()}
        return JsonResponse(
            {
                "success": False,
                "errors": errors,
            },
            status=400,
        )


class LogoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"success": True})