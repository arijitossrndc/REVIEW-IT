from django import forms
from .models import Org,Services,Admin_login
from .models import Admin, Question,Review
class login_form_org(forms.ModelForm):
	class Meta:
		model = Org
		fields = ('company','password')
	confirm_password = forms.CharField(max_length=100)

class login_form(forms.Form):
	company = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

class add_service(forms.ModelForm):
	class Meta:
		model = Services
		fields = ('company','service','category','description')

class admin_login_form(forms.Form):
	class Meta:
		model = Admin
	username = forms.CharField(max_length=10)
	password = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)

class auth_form(forms.Form):
	otp_test = forms.CharField(max_length=10)
	
class service(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('Category_id','Question')
		
class reviewform(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('Category_id','review1','review2','review3','review4','review5','comment')