from django import forms
from .models import BlogPost
from django.core.exceptions import ValidationError

class AddBlog(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields = ['title', 'Description','Blog', 'image1']

class CommentForm(forms.Form):
    
    def is_email(value):
        if "@." in value:
            pass
        else:
            raise ValidationError("Enter appropriate email")
        
    def is_message(value):
        if len(value)>0:
            pass
        else:
            raise ValidationError("This field cannot be empty")
        
    def is_name(value):
        if len(value)>0:
            pass
        else:
            raise ValidationError("This field cannot be empty")
            
    name = forms.CharField(max_length=50, validators=[is_name])
    email = forms.EmailField(max_length= 50, required=False, validators=[is_email])
    message = forms.CharField(widget=forms.Textarea, validators=[is_message])
    
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        message = cleaned_data.get('message')
    
    
            
        