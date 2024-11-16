import threading
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.core.mail import BadHeaderError,send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .utils import TokenGenerator,generate_token
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from .models import *

def home(request):
    return render(request,'home.html')

#/////////////////////////Admin Registration//////////////////////////////
def admin_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password==repassword:
            if User.objects.filter(username=username).exists():
                    messages.error(request, 'username exist')
            elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email exist')

            user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
            user.set_password(password)
            user.save()
            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')
            my_admin_group.user_set.add(user)
            mail_subject='please activate your account'
            current_site=get_current_site(request)
            message=render_to_string('account_verification.html',{'user':user,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':generate_token.make_token(user)})
            to_email=email
            send_email=EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
            EmailThread(send_email).start()
            messages.success(request, 'Account created successfully! Please check your email for activate the account .')   
            return HttpResponseRedirect('admin_login_view')
        else:
            messages.error(request, 'password donot match')
    return render(request, 'admin/admin-signup.html')

class EmailThread(threading.Thread):
    def __init__(self, send_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_email = send_email
        
    def run(self):
        self.send_email.send()


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            if user.groups.filter(name='SELLER').exists():
                messages.success(request, ' account activated successfully!')
                return redirect('admin_login_view')  
         
        else:
            messages.error(request, 'Activation link is invalid or has expired.')
        return render(request, 'account_verification.html')

    
def admin_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff and request.user.groups.filter(name='ADMIN').exists():
            return HttpResponseRedirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff and user.groups.filter(name='ADMIN').exists():
                login(request, user)
                return redirect('afterlogin_view')
            else:
                messages.error(request, 'You do not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin/admin-login.html')



def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

#///////////////////////////////////////AUTHENTICATION////////////////////////////////////////////

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    else:
        return redirect('home')

    
def handel_logout(request):
    if request.user.is_authenticated:
        logout(request)
        if request.user.groups.filter(name='ADMIN').exists():
            return redirect('admin_login_view')  
    else:
        return redirect('home')  
    return render(request,'home.html')


#///////////////////////////////principle register/////////////////////
def principleRegistration(request):
    Qualification=qualification.objects.all()
    return render(request,'principle/principle_signup.html',{'qualification':Qualification})

def principleLogin(request):
    return render(request,'principle/principle_login.html')