from django.db import models
from datetime import datetime, timedelta
from django.shortcuts import reverse
from django.db.models.fields import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
)
from django.contrib.auth.models import User
from account.models import Profile

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose, SmartResize
from django.db.models.signals import pre_save
from luumania.utils import unique_slug_generator
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
#Questions


#
#
# class Blog(models.Model):
#     User = models.CharField(max_length=100)

# MESSAGE

class Message(models.Model):
    name=models.CharField(max_length=100)
    phone=models.FloatField(default=None)
    mail=models.EmailField(default=None)
    message=models.TextField()

 #CAROUSEL CLASSES
#MEN 1 2 3
class IndexCarousel(models.Model):
    CHOICES = (('Men','Men'),
            ('Women','Women'),
            ('Kids', 'Kids'))
    Image = models.ImageField(upload_to='images', blank=True, null=True, default=None)
    Title = models.CharField(max_length=30)
    Description = models.CharField(max_length=30)
    url = models.URLField(default=None, blank=True, null=True)
    Category = models.CharField( default=None, blank=True, choices=CHOICES, null=True, max_length=200)





#ITEM

class item(models.Model):
    CHOICES = (('Men','Men'),
            ('Women','Women'),
            ('kidB', 'Kids Boy'),
            ('kidG','Kids Girl'))

    OPTIONS = (('Tops_Tshirt', 'Tops and Tshirt'),
    ('Hoodies_Sweatshirt', 'Hoodies and Sweatshirt'),
    ('Jacket_Gilets','Jacket and Gilet'),
    ('Jeans','Jeans'),
    ('Joggers','Joggers'),
    ('Shorts','Shorts'),
    ('Leathers', 'Leathers Wears'),
    ('BagPacks','BagPacks'),
    ('Accessories','Accessories'),
    ('Goldstar','Goldstar'),
    ('Canvas','Canvas'),
    ('Jerseys_Kits','Jerseys and Kits'),
    ('Sports','Sports'),
    ('Formals','Formals'),
    ('Football','Football'),
    ('Basketball','Basketball'),
    ('Sandal_Flipflop', 'Sandals and Flipflop'),
    ('Kurtha','Kurtha'),
    ('Saree','Saree'),
    ('Skirts_Pants', 'Skirts and Pants'),
    ('Dresses' , 'Dresses'),
    ('Heels','Heels'),
    ('Boots','Boots'),
    ('Close_Shoe', 'CloseShoe'),
    ('Sandals','Sandals'),
    ('ClothingB','Clothing'),
    ('FootwearsG','Footwears'),
    ('ClothingG','Clothing'),
    ('FootwearsB','Footwears')

    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')


    number = models.CharField(default=None, blank=True, null=True, max_length=55)

    username = models.CharField(max_length=150)
    price = models.FloatField()
    dis_price = models.FloatField(blank=True, null=True)
    auto_id = models.AutoField(primary_key=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    add_description = models.TextField(blank= True, null=True)
    category=models.CharField( default=None, blank=True, choices=CHOICES, null=True, max_length=200)

    subcategory=models.CharField( default=None, blank=True, choices=OPTIONS, null=True, max_length=200)

    image1 = models.ImageField(upload_to='images',)

    image2 = models.ImageField(upload_to='images', blank=True, null=True, default=None)

    image3 = models.ImageField(upload_to='images', blank=True, null=True, default=None)

    bloglink = models.CharField(default=None, null=True, blank=True, max_length=55)
    date=models.DateTimeField(auto_now=True)
    size_s = models.CharField(max_length=5, blank=True, null=True)
    size_m = models.CharField(max_length=5, blank=True, null=True)
    size_l = models.CharField(max_length=5, blank=True, null=True)
    size_xl = models.CharField(max_length=5, blank=True, null=True)
    size_xxl = models.CharField(max_length=5, blank=True, null=True)

    

    




    def __str__(self):
        return self.name


    
        

    def get_absolute_url(self):
        return reverse("content:productdetail", kwargs={
        'slug':self.slug
        })
    def get_absolute_url2(self):
        return reverse("content:productdetail1", kwargs={
        'slug':self.slug
        })
    def get_absolute_url1(self):
        return reverse("content:update", kwargs={
        'slug':self.slug
        })
    
    def get_absolute_url3(self):
        return reverse("content:comment", kwargs={
        'slug':self.slug
        })
    
    def get_add_fav_url(self):
        return reverse("content:addfavorites", kwargs={
            'slug':self.slug
        })
    def get_rem_fav_url(self):
        return reverse("content:remfavorites", kwargs={
            'slug':self.slug
        })
    def phone_number(self):
        return self.user.Phone_number
    
    def service(self):
        return self.user.Service
    
    def url(self):
        return self.user.Address_url
    
    def address(self):
        return self.user.Address
    
    def facebook(self):
        return self.user.Facebook
    
    def instagram(self):
        return self.user.Instagram
    
    def City(self):
        return self.user.City
    
    
    def get_comment_url(self):
        return reverse("content:comment", kwargs={
        'slug':self.slug
        })

def slug_generator(sender, instance, *ards, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance )

pre_save.connect(slug_generator, sender=item)








#
class BlogPost(models.Model):
    # content=HTMLField()
    username = models.CharField(max_length=150)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    username=models.CharField(max_length=200, blank=True, null=True, default=None)
    title = models.CharField(max_length=200)
    Blog = RichTextUploadingField(blank=True, null=True, default=None)
    UserImage = models.ImageField(upload_to='images',blank=True, default=None, null=True)
    image1 = models.ImageField(upload_to='images',blank=True, null=True)
    image2 = models.ImageField(upload_to='images',blank=True, null=True)
    image3 = models.ImageField(upload_to='images',blank=True, null=True)
    date=models.DateTimeField(auto_now=True)
    elong=models.BooleanField(default=False, blank=True, null=True)
    slug= models.SlugField(blank=True, null=True)
    item_slug = models.CharField(max_length=200 ,blank=True, default=None, null=True)
    Description = models.CharField(max_length=40, default=None)
    
    
    def UserImage(self):
        return self.user.image1

    def get_absolute_url(self):
        return reverse("content:blog", kwargs={
        'slug':self.slug
        })
    
    def get_delete_url(self):
        return reverse("content:blog_delete", kwargs={
        'slug':self.slug
        })
        
        
    
   
        
        


def slug_generator1(sender, instance, *ards, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance )

pre_save.connect(slug_generator1, sender=BlogPost)



class CImage(models.Model):
    CHOICES = (('Men','Men'),
            ('Women','Women'),
            ('Kids', 'Kids'))

    Image = models.ImageField(upload_to='images', default=None, blank=True, null=True)
    Title=models.CharField(max_length=100, default=None, blank=True, null= True)
    Category = models.CharField( default=None, blank=True, choices=CHOICES, null=True, max_length=200)



class Dealcarousel(models.Model):

    title = models.CharField(max_length=100, default=None, blank=True, null= True)
    image = models.ImageField(upload_to='images',default=None, blank=True, null=True)


class Shopview(models.Model):
    title = models.CharField(max_length=100, default=None, blank=True, null= True)
    image = models.ImageField(upload_to='images',default=None, blank=True, null=True)
    site=models.URLField(default=None, blank=True,null=True)
    
    

class Comment(models.Model):
    Object = models.ForeignKey(item, on_delete=models.CASCADE)
    User = models.ForeignKey(Profile, on_delete=models.CASCADE)
  
    Name = models.CharField(max_length=50, default=None, blank=True, null=True)
    Email = models.EmailField(max_length=50, default=None, blank=True, null=True)
    Message = models.TextField(max_length=200)
    
    def get_delete_url(self):
        return reverse("content:comment_delete", kwargs={
        'id':self.id, 'slug':self.Object.slug
        })
        
    

    

class FeaturedProduct(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    title = models.CharField(default=None, max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images',blank=True, default=None, null=True)
    description = models.CharField(max_length=50,default=None)
    url = models.URLField(default=None)
    category = models.CharField(default=None, max_length=50)
    
class Favorite(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def price(self):
        return self.item.price
    
    def name(self):
        return self.item.name
    
    def url(self):
        return self.item.get_absolute_url
    
    def image(self):
        return self.item.image
        