from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from app.models import Client
from app.utils import initial_mail_adding


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        try:
            client = Client()
            client.client_id = request.POST['client-key']
            client.client_secret = request.POST['client-secret']
            client.access_token = request.POST['access-token']
            client.client_url = request.POST['host']
            if initial_mail_adding(client):
                client.save()
                messages.success(request, 'Your instance was successfully added.', extra_tags='alert-success')
            else:
                messages.error(request, 'Something wennt wrong adding your instance!', extra_tags='alert-danger')
        except IntegrityError as e:
            messages.error(request, 'This instance already exists in our database!', extra_tags='alert-danger')

        return redirect('home')
