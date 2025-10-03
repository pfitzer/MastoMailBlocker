from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from app.exception import MastodonException
from app.mastodon import Mastodon
from app.models import Client, Faq


class HomeView(TemplateView):
    """

    The `HomeView` class is a Django view that handles the rendering of the home page and the submission of a form.

    Attributes:
        None

    Methods:
        - `get(self, request, *args, **kwargs)`:
            - This method is called when a GET request is made to the `HomeView` view.
            - It renders the 'index.html' template.
            - Parameters:
                - `request`: The `HttpRequest` object representing the incoming request.
                - `*args`: Additional positional arguments.
                - `**kwargs`: Additional keyword arguments.
            - Returns:
                - The rendered `index.html` template.

        - `post(self, request, *args, **kwargs)`:
            - This method is called when a POST request is made to the `HomeView` view.
            - It handles the form submission and registration logic.
            - Parameters:
                - `request`: The `HttpRequest` object representing the incoming request.
                - `*args`: Additional positional arguments.
                - `**kwargs`: Additional keyword arguments.
            - Returns:
                - If the registration is successful, it redirects the user to the authorization URL returned by the Mastodon client.
                - If there is a database integrity error, it displays an error message.
                - If any other exception occurs, it displays an error message.
                - In all cases, it redirects the user back to the home page.

    """

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        try:
            redirect_url = self._handle_form_submission(request)
            return redirect(redirect_url)
        except IntegrityError:
            messages.error(request, 'This instance already exists in our database!', extra_tags='alert-danger')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}", extra_tags='alert-danger')
        return redirect('home')

    def _handle_form_submission(self, request):
        client = self._create_client(request)
        mastodon = Mastodon(client=client)
        self._register_application(client, mastodon, request)
        return mastodon.get_authorization_url(request)

    @staticmethod
    def _create_client(request):
        """Create a client with only URL initially. OAuth fields populated later."""
        client_url = request.POST.get('host', '').strip()

        # Normalize URL
        if client_url and not client_url.startswith(('http://', 'https://')):
            client_url = f'https://{client_url}'

        client = Client.objects.create(
            client_url=client_url.rstrip('/')
        )
        return client

    @staticmethod
    def _register_application(client, mastodon, request):
        client_key, client_secret = mastodon.register_app(request)
        client.client_key = client_key
        client.client_secret = client_secret
        client.save()


class FaqView(ListView):
    """
    A class that represents a view for displaying frequently asked questions (FAQs).

    Attributes:
        template_name (str): The name of the template file to be rendered for this view.
        model (Model): The model class for the FAQs.
        context_object_name (str): The name of the context variable in the template that holds the FAQs.

    """
    template_name = 'faq.html'
    model = Faq
    context_object_name = 'faqs'


def get_code(request, client_id):
    """
    Gets the code from the request parameters, obtains an access token using the Mastodon client,
    saves the access token to the client object, and redirects the user to the home page.

    Parameters:
        request (HttpRequest): The HTTP request object containing the parameters.
        client_id (int): The ID of the client object to update.

    Returns:
        HttpResponseRedirect: The redirect response to the home page.

    """
    if request.GET.get('code'):
        code = request.GET.get('code')
        try:
            client = Client.objects.get(pk=client_id)
            mastodon = Mastodon(client=client)
            client.access_token = mastodon.obtain_access_token(code, request)
            client.save()
            mastodon.auth_ready()
            messages.success(request, 'Your instance was successfully added.', extra_tags='alert-success')
        except Client.DoesNotExist:
            create_error_message(request, "This client does not exist.")
        except MastodonException as e:
            create_error_message(request, str(e))

    else:
        create_error_message(request, "An error occurred getting the access token from your instance")
    return redirect('home')


class DisclaimerView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'disclaimer.html')


class ImprintView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'impressum.html')


def create_error_message(request, msg: str):
    messages.error(request, msg, extra_tags='alert-danger')
