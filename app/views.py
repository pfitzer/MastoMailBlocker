from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from mastodon import Mastodon

from app.models import Client


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.GET.get('code') and request.session.get('client_id'):
            client = Client.objects.get(pk=request.session.get('client_id'))
            client.client_code = request.GET.get('code')
            client.save()
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        m = Mastodon.create_app('MastoMailBlocker', scopes=['admin:write:email_domain_blocks'], api_base_url=request.POST['host'], redirect_uris='http://localhost:8000')
        try:
            client = Client()
            client.client_id = m[0]
            client.client_secret = m[1]
            client.client_url = request.POST['host']
            client.save()
        except IntegrityError as e:
            messages.error(request, 'This host already exists in the database')
            return redirect('home')

        mast = Mastodon(client_id=client.client_id, client_secret=Client.client_secret, api_base_url=client.client_url)
        url = mast.auth_request_url(client_id=client.client_id, scopes=['admin:write:email_domain_blocks'], redirect_uris='http://localhost:8000')
        if url:
            request.session['client_id'] = client.pk
            return redirect(url)
        return render(request, 'index.html')

