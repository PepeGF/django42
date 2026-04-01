from django.utils import timezone
from django.conf import settings
import random


class AnonymousSessionMiddleware:
    """Ensure each visitor has an anonymous name stored in session for 42 seconds."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        anon_name = request.session.get('anon_name')
        anon_expires = request.session.get('anon_expires')
        now = timezone.now().timestamp()
        if not anon_name or not anon_expires or now > anon_expires:
            names = getattr(settings, 'ANON_NAMES', None)
            if not names:
                names = ['Alpha','Bravo','Charlie','Delta','Echo','Foxtrot','Golf','Hotel','India','Juliet']
            chosen = random.choice(names)
            request.session['anon_name'] = chosen
            request.session['anon_expires'] = now + 42
        response = self.get_response(request)
        return response
