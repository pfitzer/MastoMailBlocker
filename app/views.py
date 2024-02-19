from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from app.models import Client, Faq


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        try:
            self._create_client(request)
        except IntegrityError:
            messages.error(request, 'This instance already exists in our database!', extra_tags='alert-danger')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}", extra_tags='alert-danger')
        return redirect('home')

    def _create_client(self, request):
        client = Client()
        client.client_id = request.POST['client-key']
        client.client_secret = request.POST['client-secret']
        client.access_token = request.POST['access-token']
        client.client_url = request.POST['host']
        client.save()
        messages.success(request, 'Your instance was successfully added.', extra_tags='alert-success')


class FaqView(ListView):
    template_name = 'faq.html'
    model = Faq
    context_object_name = 'faqs'