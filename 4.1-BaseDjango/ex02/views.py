from django.shortcuts import render
from .forms import SampleForm

# Create your views here.

def form_view(request):
    """Handle form display and submission."""
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return render(request, 'ex02/success.html', {'name': name})
    else:
        form = SampleForm()
    
    return render(request, 'ex02/form.html', {'form': form})