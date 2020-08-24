from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect
from django.http import *
from .forms import SignUpForm, UserLoginForm, UpdateForm, SignUpUser
from .models import SignUp,Profile
from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


from django.http import HttpResponseRedirect

# Create your views here.
def signup(request):
    form=SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
                name = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                confirm = form.cleaned_data.get('confirm')
                E_Sewa = form.cleaned_data.get('E_Sewa')
                Phone_number = form.cleaned_data.get('Phone_number')
                Address = form.cleaned_data.get('Address')
                Address_url = form.cleaned_data.get('Address_url')
                E_mail = form.cleaned_data.get('E_mail')
                choice = form.cleaned_data.get('Delivery_Service')
                shopkeeper = form.cleaned_data.get('Shopkeeper')
                
                
                data = SignUp(username=name, password=password, comfirm=confirm, E_sewa=E_Sewa, Phone_number=Phone_number, Address=Address,
                                Address_url=Address_url, E_mail=E_mail, Service=choice, Shopkeeper=shopkeeper)
                                
                data.save()
                return redirect('/account/register')

    return render(request,'signup.html', {'form': form} )

def signup_user(request):
    if request.method == 'POST':
        form = SignUpUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            Profile.objects.create(user=user)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpUser()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
    
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        name={'username':username}

        if user is not None:
            auth.login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                if (request.user.profile.type == "shop" or request.user.profile.type == "blog"):
                    return redirect('/welcome')
                else:
                    return redirect('/')
        else:
            context = {
            'form': form, 'error' : "Your credentials do not match with us. Make sure you enter both the fields corectly."
            }
            return render(request, "login.html", context)
    context={'form':form}
    return render(request, "login.html", context)




@login_required(login_url="/accounts/login")
def logout_view(request):
    logout(request)

    return redirect('/')

@login_required(login_url="/accounts/login")
def update(request):
    form=UpdateForm()
    username=request.user.username
    user=Profile.objects.filter(user=request.user)
    
  



    if request.method == 'POST':

        form = UpdateForm(request.POST, request.FILES )

        if form.is_valid():
            user=request.user
            username = request.user.username
            
            for i in Profile.objects.all():
                if (i.username == username):
                    Fname = form.cleaned_data.get('Fname')
                    Lname = form.cleaned_data.get('Lname')
                    Address = form.cleaned_data.get('Address')
                    Contact = form.cleaned_data.get('Contact')
                    Facebook = form.cleaned_data.get('Facebook')
                    Instagram = form.cleaned_data.get('Instagram')
                    Email = form.cleaned_data.get('E_mail')
                    Userpic = form.cleaned_data.get('Profile')

                    if (Fname==""):
                        pass
                    else:
                        i.First_name=Fname
                    if (Lname==""):
                        pass
                    else:
                        i.Last_name=Lname
                    if (Contact==""):
                        pass
                    else:
                        i.Phone_number=Contact
                    if (Address==""):
                        pass
                    else:
                        i.Address_per = Address
                    if (Facebook==""):
                        pass
                    else:
                        i.Facebook = Facebook
                    if (Instagram==""):
                        pass
                    else:
                        i.Instagram = Instagram
                    if Userpic is None:
                        pass
                    else:
                        i.Image1= Userpic

                    if (Email==""):
                        pass
                    else:
                        user.email=Email
                        user.save()
                    i.save()

                    
                    context={'form':form, 'user':i}
                    return redirect('/accounts/update_account')


                



    context={'form':form, 'user':user}
    return render(request, 'updateinfo.html', context)


def del_user(request):
    user=request.user
    user.delete()
    return redirect('/')
