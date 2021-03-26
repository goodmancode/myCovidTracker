from django.http import HttpResponse
from django.shortcuts import render
from mycovidtracker.backend import send_risk_to_database

def index(request):
	return render(request, 'index.html')

def submit(request): 
	if request.method == 'POST':
		uid = request.POST.get('uid')
		

		send_risk_to_database(str(uid))
		
		
	return HttpResponse('')
