from django.contrib import admin
from .models import item, Message,IndexCarousel,BlogPost, CImage, Dealcarousel, Shopview, Comment, FeaturedProduct, Favorite
# Register your models here.
class ItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'username')
    search_fields = ('username',)
    # list_filter = ('username', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()





admin.site.register(item, ItemAdmin)
admin.site.register(Message)

admin.site.register(IndexCarousel)
admin.site.register(BlogPost)
admin.site.register(Favorite)
admin.site.register(CImage)
admin.site.register(Dealcarousel)
admin.site.register(Comment)
admin.site.register(Shopview)
admin.site.register(FeaturedProduct)
