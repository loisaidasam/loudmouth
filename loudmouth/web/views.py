# Library
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# Project
from loudmouth.core.models import IncomingEmail, EmailRating

@login_required
def index(request):
	if request.method == 'POST':
		email_id = request.POST.get('email_id')
		rating = request.POST.get('rating')
		try:
			email = IncomingEmail.objects.get(id=email_id)
			
			try:
				rating_row = EmailRating.objects.get(user=request.user, email=email)
				rating_row.rating = rating
				rating_row.save()
			except EmailRating.DoesNotExist:
				rating_row = EmailRating.objects.create(
					user=request.user,
					email=email,
					rating=rating,
				)
		except IncomingEmail.DoesNotExist:
			pass
	
	show_all = int(request.REQUEST.get('show_all', 0))
	
	context = {
		'show_all': show_all,
		'emails': IncomingEmail.objects.get_user_emails(request.user, show_all=show_all),
	}
	return render_to_response('index.html', context, RequestContext(request))

@login_required
def hallofshame(request):
	shamers = EmailRating.objects.get_shamers()
	if shamers:
		high_shamer = shamers[0]
	else:
		high_shamer = None
	context = {
		'shamers': shamers,
		'high_shamer': high_shamer,
	}
	return render_to_response('hallofshame.html', context, RequestContext(request))
