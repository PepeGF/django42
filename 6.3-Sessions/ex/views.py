from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Tip, Vote
from .forms import TipForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout as auth_logout
from django.contrib import messages



def home(request):
	# Anonymous session name (42 seconds validity)
	anon_name = request.session.get('anon_name')
	anon_expires = request.session.get('anon_expires')
	now = timezone.now().timestamp()
	if not anon_name or not anon_expires or now > anon_expires:
		import random
		names_list = ['Alpha','Bravo','Charlie','Delta','Echo','Foxtrot','Golf','Hotel','India','Juliet']
		chosen = random.choice(names_list)
		request.session['anon_name'] = chosen
		request.session['anon_expires'] = (timezone.now().timestamp() + 42)
		anon_name = chosen

	tips = Tip.objects.select_related('author').all().order_by('-created_at')
	form = TipForm()
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return redirect('ex:home')
		form = TipForm(request.POST)
		if form.is_valid():
			tip = form.save(commit=False)
			tip.author = request.user
			tip.save()
			return redirect('ex:home')

		# Show messages if present
		msg = request.GET.get('msg')
		if msg:
			messages.info(request, msg)

	ctx = {
		'anon_name': anon_name,
		'tips': tips,
		'form': form,
	}
	return render(request, 'ex/home.html', ctx)


@login_required
def vote(request, tip_id, value):
	tip = get_object_or_404(Tip, pk=tip_id)
	value = 1 if int(value) == 1 else -1
	# Check downvote permission
	if value == -1 and not (tip.author == request.user or getattr(request.user, 'can_downvote', lambda: False)()):
		messages.error(request, 'You are not allowed to downvote yet.')
		return redirect('ex:home')

	vote_obj, created = Vote.objects.get_or_create(tip=tip, user=request.user, defaults={'value': value})
	if not created:
		if vote_obj.value == value:
			# toggle off
			vote_obj.delete()
		else:
			vote_obj.value = value
			vote_obj.save()
	return redirect('ex:home')


@login_required
def delete_tip(request, tip_id):
	tip = get_object_or_404(Tip, pk=tip_id)
	# For now, allow author to delete; later enforce permissions
	if tip.author == request.user or getattr(request.user, 'can_delete_tips', lambda: False)() or request.user.has_perm('ex.delete_tip'):
		tip.delete()
	return redirect('ex:home')


def register(request):
	if request.user.is_authenticated:
		return redirect('ex:home')
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('ex:home')
	else:
		form = UserCreationForm()
	return render(request, 'ex/register.html', {'form': form})


def login_view(request):
	if request.user.is_authenticated:
		return redirect('ex:home')
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('ex:home')
	else:
		form = AuthenticationForm()
	return render(request, 'ex/login.html', {'form': form})


def logout_view(request):
	auth_logout(request)
	return redirect('ex:home')
