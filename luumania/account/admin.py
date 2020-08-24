from django.contrib import admin

from .models import SignUp,Profile
# Register your models here.
class SignUpAdmin(admin.ModelAdmin):

    list_display = ('username',)
    search_fields = ('username',)
    # list_filter = ('username', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(SignUp, SignUpAdmin)
admin.site.register(Profile)
