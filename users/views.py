from django.views.generic import CreateView
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/index/"
    template_name = "signup.html"
