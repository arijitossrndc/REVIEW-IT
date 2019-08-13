from django.shortcuts import render,redirect,HttpResponse
from .forms import login_form_org,login_form,add_service,service,reviewform
from .forms import admin_login_form,auth_form
from .models import Org,Services,Admin,Question,Category,Review
import random
from django.http import Http404
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
# Create your views here.
def main(request):

	return render(request,'index.html')
	
def create(request):

	if request.method == 'GET':
		
		form = login_form_org()

		return render(request,'login_org.html',{'form':form})

	if request.method == 'POST':
		form = login_form_org(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']
			if(password==confirm_password):
				form.save()
				form = login_form_org()
				success = "Registered success"
				context = {
				'not':success,
				'form':form
				}
			else:
				form = login_form_org()
				error = "password and confirm password doesnot not match"
				context={
				'not':error,
				'form':form
				}
		
		return render(request,'login_org.html',context)
	
def login(request):

	form = login_form()

	if request.method =='GET':
		if request.session.has_key('company'):
			username = request.session['company']
			context = {
				'username':username,
				}
			return redirect("/homepage")
		else:
			error = "Please login"
			context = {
			'form':form
			}
			return render(request,'login.html',context)
	else:
		form = login_form(request.POST)
		if form.is_valid():
			company = form.cleaned_data['company']
			password = form.cleaned_data['password']
			Check = Org.objects.filter(company=company,password=password).count()
			if(Check>=1):
				request.session['company'] = company
				context = {
				'username':company
				}
				return redirect('/homepage')
			else:
				error = "Please login"
				context = {
				'error':error
				}
				return redirect('/homepage')

def logout(request):
	form =login_form()
	del request.session['company']
	context={
	'form':form
	}
	return redirect('/login')

def homepage(request):
	if request.session.has_key('company'):
		form = add_service()
		categorys = Category.objects.all()
		username = request.session['company']
		query_set = Services.objects.filter(company=username,status="A")
		context = {
		'objects': query_set,
		'username':username,
		'form':form,
		'categorys': categorys
		}
		return render(request,'test.html',context)
	else:
		return redirect('/login')

def add_service_form(request):
	form = add_service(request.POST)
	username = request.session['company']
	if form.is_valid():
		company = form.cleaned_data['company']
		service = form.cleaned_data['service']
		category = form.cleaned_data['category']
		description = form.cleaned_data['description']
		if(company==username):
			form.save()
		else:
			return HttpResponse(form)
		return redirect('/homepage')
	
def myservice(request,id):
	if request.session.has_key('company'):
		username = request.session['company']
		query_set = Services.objects.get(id=id)
		return render(request,'myservice.html',{'object':query_set,'username':username})

def admin_login(request):
	if request.method == 'GET':
		form = admin_login_form()
		return render(request,'login_admin.html',{'form':form})
	else:
		form = admin_login_form(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			Check = Admin.objects.filter(username=username,password=password,email=email).count()
			if(Check>=1):
				request.session['username'] = username
				otp = random.randint(50000,70000)
				request.session['otp'] = otp
				subject='Hey Admin'
				message='This is your OTP to login '+str(otp)
				from_email=settings.EMAIL_HOST_USER
				to_email = [email]
				send_mail(subject=subject,from_email=from_email,recipient_list=to_email,message=message,fail_silently=False)
				return redirect('/auth')
			else:
				error = "Username or password invalid!!!!"
				context = {
				'error':error,
				'form':form
				}
				return render(request,'login_admin.html',context)

def auth(request):
	if request.method == 'GET':
		if request.session.has_key('otp'):
			if(request.session.has_key('admin_verify') and request.session['admin_verify'] == "1"):
				return redirect('/admin_home')
			else:
				form = auth_form()
				otp = request.session['otp']
				return render(request,'auth.html',{'form':form,'otp':otp})
		else:
			return HttpResponse("Page does not exist")
	else:
		form = auth_form(request.POST)
		if form.is_valid():
			otp = request.session['otp']
			otp1 = form.cleaned_data['otp_test']
			otp1 = int(otp1)
			if(otp1==otp):
				request.session['admin_verify'] = "1"
				return redirect('/auth')
			else:
				del request.session['otp']
				del request.session['username']
				return redirect('/admin_login')

def admin_home(request):
	pendingServiceRequest = Services.objects.filter(status="P")
	context = {
		'pending_services': pendingServiceRequest 
	}
	return render(request,'auth_admin.html', context)

def accept_service(request):
	company = request.GET['company']
	service = request.GET['service']
	category = request.GET['category']
	update = Services.objects.filter(company=company,service=service,category=category).update(status='A')
	pendingServiceRequest = Services.objects.filter(status="P")
	context = {
		'pending_services': pendingServiceRequest 
	}
	return render(request, 'acceptRejectDiv.html', context)

def reject_service(request):
	company = request.GET['company']
	service = request.GET['service']
	category = request.GET['category']
	update = Services.objects.filter(company=company,service=service,category=category).update(status='R')
	pendingServiceRequest = Services.objects.filter(status="P")
	context = {
		'pending_services': pendingServiceRequest 
	}
	return render(request, 'acceptRejectDiv.html', context)

def service_category(request):
	all_cattegories = Category.objects.all()
	context = {
		'categories': all_cattegories
	}
	return render(request, 'service_category_home.html', context)
	# return HttpResponse('hey there crud for service category here !!!')

def add_category(request):
	category_name = request.POST['service_category']
	c = Category(name = category_name)
	c.save()
	return redirect('/admin_service_category')

def delete_category(request):
	category_id = request.POST['service_category']
	Category.objects.filter(id=category_id).delete()
	return redirect('/admin_service_category')

def service_question(request):
	if request.method == 'POST':
		form = service(request.POST)
		if form.is_valid():
			Category_id = form.cleaned_data['Category_id']

			Question = form.cleaned_data['Question']
			form.save()
	all_category = Category.objects.all()
	context = {
		'categorys': all_category
	}
	return render(request, 'service_question_home.html', context)

def search(request):
	if request.method =='POST':
		search = request.POST['Search']
		print(search)
		result = Org.objects.filter(company__contains=search)
		print(result)	
		values_list = list(result.values('id','company'))
		return JsonResponse(values_list,safe=False)
		
def review(request):
	if request.method =='POST':
		company = request.POST['company']
		company_services = Services.objects.filter(company=company, status='A')
		context = {
			'services': company_services,
			'company_name': company 
		}

	return render(request, 'service_category_review.html', context)

def get_question(request):
	company = request.GET['company']
	service = request.GET['service']
	category = Services.objects.filter(company=company,service=service).first().category
	all_questions = Question.objects.filter(Category_id=category)
	context = {
		'questions': all_questions 
	}
	return render(request, 'question_div.html', context)


def category_review(request):

	form = reviewform(request.POST)

	if request.method == 'POST':
		if form.is_valid():
			Category_id=form.cleaned_data['Category_id']
			review1=form.cleaned_data['review1']
			review2=form.cleaned_data['review2']
			review3=form.cleaned_data['review3']
			review4=form.cleaned_data['review4']
			review5=form.cleaned_data['review5']
			comment=form.cleaned_data['comment']

			form.save()

	return redirect('/review_service')


		