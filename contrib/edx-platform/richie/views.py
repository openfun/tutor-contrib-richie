from urllib.parse import urljoin


from django.conf import settings
from django.shortcuts import redirect


def redirect_to_richie(request, subpath):
    """
    Redirect to Richie catalog.

    This view is used after login from Richie, with a "?next=richie/en"
    parameter.
    """
    return redirect(urljoin(settings.RICHIE_ROOT_URL, subpath))
