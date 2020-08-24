from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpUser(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class SignUpForm(forms.Form):
    

    def is_special(pwd):
        
        if any(char in "1234567890!@#$%^&*" for char in pwd):
            pass
        else:
            raise ValidationError("Password must contain special characters or numbers.")
        if len(pwd) < 8:
            raise ValidationError("Password must contain minimum of 8 characters.")
        else:
            pass
             
    
    def is_number(value):
        try:
            value = int(value)
        except:
            raise ValidationError("Must only contain numbers.")
    
   
        
    
    error_css_class = "error"
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Username')
    E_mail = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label="E-mail")
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class' : 'field'
    }),label='Password', validators=[is_special])
    confirm = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class' : 'field'
    }),label='Confirm-Password')
    E_Sewa = forms.CharField(max_length=10,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='E-sewa', validators=[is_number])
    Phone_number = forms.CharField(max_length=10,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Phone number', validators=[is_number])
    Address = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Address')
    Address_url = forms.URLField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }), required=False)
    CHOICES=[('True','Yes'),
         ('False','No')]

    Delivery_Service = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    Shopkeeper = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


    
        


    def clean(self):
        
        cleaned_data = super(SignUpForm, self).clean()
        name = cleaned_data.get('username')
        for i in User.objects.all():
            if name == i.username:
                self.add_error('username',"username exists")
            else:
                pass
        
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')
        if password == confirm:
            pass
        else:
            self.add_error('password',"password you entered do not match")
            self.add_error('confirm',"password you entered do not match")
        
       
                                
        
        

        

class UpdateForm(forms.Form):
    CITY_CHOICES = (('Kathmandu','Kathmandu'),
                    ('Pokhara','Pokhara'),
                    ('Biratnagar', 'Biratnagar'),
                    ('Bhaktapur','Bhaktapur'),
                    ('Lalitpur','Lalitpur'),
                    ('Nepalgunj','Nepalgunj'))
    
    def is_number(value):
        try:
            value = int(value)
        except:
            raise ValidationError("Must only contain numbers.")
    E_mail = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label="E-mail", required=False)
    Fname= forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='First Name', required=False)
    Lname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label="Last Name", required=False)
    Address = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Address', required=False)
    Contact = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Contact Number', required=False, validators=[is_number])
    Facebook = forms.URLField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Facebook (Url)', required=False)
    Instagram = forms.URLField(max_length=200,widget=forms.TextInput(attrs={
    'class' : 'field'
    }),label='Instagram (Url)', required=False)
    Profile=forms.ImageField(label='Profile Image', required=False)
    City=forms.CharField(max_length=200, required=False, widget=forms.Select(choices=CITY_CHOICES))


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'field'
    }), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class' : 'field'
    }), label='Password')
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')




        return super(UserLoginForm, self).clean(*args, **kwargs)

