from django.shortcuts import render, redirect
from .forms import History
import logging
from django.conf import settings

logger = logging.getLogger("form_logger")

def form_view(request):
    """Handle form display and submission."""
    if request.method == 'POST':
        form = History(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            logger.info("%s", text)
            return redirect('ex02-form') # este el el nombre de la url puesto en urls.py de la app
    else:
        try:
            with open(settings.FORM_LOG_FILE, 'r') as f:
                log_content = f.read()
            complete_history = log_content.splitlines()
            complete_history.reverse()
        except FileNotFoundError:
            complete_history = []
        form = History()
    
    return render(
        request, 
        'ex02/form.html', 
        context={
            'form': form, 
            'history': complete_history
            }
        )
