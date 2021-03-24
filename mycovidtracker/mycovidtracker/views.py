from django.http import HttpResponse
from django.shortcuts import render
from . import submit_button

def index(request):
#  return HttpResponse('index')
	return render(request, 'index.html')

def submit(request): 
	#uid = request.POST.get('submission')
	#submit_button.button(uid)
	
	if request.method == 'POST':
		uid = request.POST.get('uid')
		
		submit_button.button(uid)
		
	return HttpResponse('')		
	#return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
	#return render(request, 'index.html')
