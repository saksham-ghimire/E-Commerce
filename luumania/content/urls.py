"""Maccount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Example
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
from .views import(
IndexView,
Menfilter,
Womenfilter,
Kidfilter,
Menfilter_s,
Womenfilter_s,
Kidfilter_s,


ItemDetailView,
ItemDetailView_s,
ItemUpdate,



search_view,
search_view_s,

view_data,

BlogView,
BlogDetailView,

userview,
filter_view,
)
app_name = 'content'
urlpatterns = [
    path('shop', views.IndexView.as_view() , name='index' ),
    path('user/<user>', views.userview.as_view(), name="user"),
    # Welcome Template
    path('started', views.blog, name="started"),
    path('add_post', views.post_add, name="posts"),
    path('blog', views.BlogView.as_view(), name="data form"),
    path('blog/<slug>/', views.BlogDetailView.as_view(), name="blog"),
    path('view_data', views.view_data.as_view(), name="data_view"),
     path('data', views.data, name="add_content"),
     path('products/<slug>/', views.ItemDetailView.as_view(), name="productdetail"),
     path('product_s/<slug>/', views.ItemDetailView_s.as_view(), name="productdetail1"),
     path('delete', views.delete_view, name="delete_detail"),
     path('contact', views.contact, name='contact'),
     path('welcome', views.welcome, name='welcome'),

     #Update
     path('update/<slug>/', login_required(views.ItemUpdate.as_view()), name="update"),
     path('comment/<slug>', views.add_comment , name="comment"),
    
     # filter
     path('filter', views.filter_view.as_view(), name='filter'),


     #search Navbar
     path('search_', views.search_view.as_view(), name='search'),
     
     path('blog/search_', views.Blog_SearchView.as_view(), name='Blog search'),
     path('search_s',views.search_view_s.as_view(), name='search'),
     path('contact', views.contact, name="contact"),
     path('contact_us', views.contact_us, name="contact"),

     

     path('Men/<name>', views.Menfilter.as_view()),
     path('Women/<name>', views.Womenfilter.as_view()),

     path('Kids/<name>', views.Kidfilter.as_view()),

     path('Men_s/<name>', views.Menfilter_s.as_view()),
     path('Women_s/<name>', views.Womenfilter_s.as_view()),

     path('Kids_s/<name>', views.Kidfilter_s.as_view()),




     #test path
      path('', views.test, name="test"),
      
      #Favorites
      
      path('favorites', views.favorites, name="favorites"),
      path('add-favorites/<slug>', views.add_fav, name="addfavorites"),
      path('rem-favorites/<slug>', views.rem_fav, name="remfavorites"),
      
      #comment-delete
      path('del_comment/<id>/<slug>', views.del_comment, name="comment_delete"),
      
      #blog-delete
      path('del_blog/<slug>', views.del_blog, name="blog_delete"),
]
