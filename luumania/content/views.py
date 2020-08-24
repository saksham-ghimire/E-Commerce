from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import item
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, reverse
from django.urls import reverse, resolve
from django.http import Http404
from django.contrib.auth.models import User
from .models import Message, IndexCarousel,BlogPost, CImage, Dealcarousel, Shopview, Comment, FeaturedProduct, Favorite
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail, EmailMultiAlternatives 

# from django.contrib.auth.models import User
from PIL import Image
from .forms import AddBlog, CommentForm
from account.models import Profile

# from .filters import filter
# Create your views here.

def test(request):
    carousel = Dealcarousel.objects.all()[1:]
    carousel1 = Dealcarousel.objects.all()[:1]
    featured = FeaturedProduct.objects.all()
    shops=Shopview.objects.all()
    carouselobj = {'carousel1':carousel1, 'carousel':carousel, 'shops':shops, 'featured':featured}
    return render(request, 'test.html', carouselobj)

def blog(request):
    return render(request, 'blog.html')

@login_required(login_url='/accounts/login')
def favorites(request):
    if request.user:
        user = request.user
        data = Favorite.objects.filter(user=user)
        context = {'data':data}
        return render (request, 'favorites.html', context)
    else:
        return redirect('/accounts/login')
        

@login_required(login_url='/accounts/login')
def add_fav(request, slug):
    get_item = get_object_or_404(item, slug=slug)
    get_user = request.user
    if get_user.is_authenticated:
        fav = Favorite(item=get_item, user=get_user)
        filter = Favorite.objects.filter(item=get_item, user=get_user)
        if filter:
            return redirect("content:productdetail", slug=slug)
        else:
            fav.save()
            return redirect("content:productdetail", slug=slug)
    
        
@login_required(login_url='/accounts/login')
def rem_fav(request, slug):
    get_item = get_object_or_404(item, slug=slug)
    get_user = request.user
    if get_user.is_authenticated:
        filter = Favorite.objects.filter(item=get_item, user=get_user)
        if filter:
            filter.delete()
            return redirect("content:productdetail", slug=slug)
        else:
            return redirect("content:productdetail", slug=slug)

        
        
        
    
def contact(request):
    return render (request, 'contact.html')

def contact_us(request):
    if request.method=="POST":
        name=request.POST['username']
        phone=request.POST['phone']
        mail=request.POST['email']
        message=request.POST['message']

        new = Message(name=name,phone=phone,mail=mail,message=message)
        new.save()
        
        return redirect('/contact')

    return render (request, 'contact.html')


class search_view(ListView):
    model = item



    def get(self, request):
        if 'search' in request.GET:
            search_term = request.GET['search']
            object_list = item.objects.filter(name__icontains=search_term).order_by('-date')
            Men  = CImage.objects.filter(Category="Men")
            Women  = CImage.objects.filter(Category="Women")
            Kids = CImage.objects.filter(Category="Kids")
            object_list = {'object_list':object_list,'Men':Men,'Women':Women,'Kids':Kids}
            return render(request, 'index.html', object_list )


class filter_view(ListView):
    model = item
    template_name = "index.html"

    def get_queryset(self):
        min = self.request.GET.get('min' )
        max=self.request.GET.get('max')
        categories = self.request.GET.get('major')
        subcategories = self.request.GET.get('minor')

        if categories=="Womens":
            categories = "Women"
        elif categories=="Mens":
            categories = "Men"

        itemobj = item.objects.filter(price__gte=min, price__lte=max, category=categories, subcategory=subcategories, City=region).order_by('-date')
        return itemobj
    def get_context_data(self, **kwargs):
        context = super(filter_view, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['Men']  = CImage.objects.filter(Category="Men")
        context['Women']  = CImage.objects.filter(Category="Women")
        context['Kids']  = CImage.objects.filter(Category="Kids")
        context ['list'] = list
        context ['lists'] = lists
        return context


class search_view_s(ListView):
    model = item



    def get(self, request):
        if 'search' in request.GET:
            username=request.user.username
            search_term = request.GET['search']
            object_list = item.objects.filter(name__icontains=search_term, username = username)
            object_list = {'object_list':object_list}
            return render(request, 'index3.html', object_list )



class IndexView(ListView):
    model = item, CImage

    queryset = item.objects.order_by('-date')
    paginate_by=2
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['Men']  = CImage.objects.filter(Category="Men")
        context['Women']  = CImage.objects.filter(Category="Women")
        context['Kids']  = CImage.objects.filter(Category="Kids")
        context ['list'] = list
        context ['lists'] = lists
        return context




class BlogView(ListView):
  template_name = 'posts.html'
  queryset=BlogPost.objects.order_by('-date')
  paginate_by=2


class Blog_SearchView(ListView):
    model = BlogPost



    def get(self, request):
        if 'search' in request.GET:
            search_term = request.GET['search']
            object_list = BlogPost.objects.filter(title__icontains=search_term).order_by('-date')
            object_list = {'object_list':object_list}
            return render(request, 'posts.html', object_list )





class BlogDetailView(DetailView):
    model=BlogPost
    template_name = "blogdetail.html"


class ItemDetailView(DetailView):
    model=item
    template_name = "product.html"
    
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        price_min = self.object.price - 1000
        price_max = self.object.price + 1000
        user_p = self.request.user.profile
        context['like'] = item.objects.filter(~Q(auto_id = self.object.auto_id),category=self.object.category, subcategory=self.object.subcategory,price__gte=price_min, price__lte=price_max)[:3]
        context ['comments'] = Comment.objects.filter(~Q(User = user_p),Object=self.get_object())
        context ['self_comments'] = Comment.objects.filter(User = user_p ,Object=self.get_object())
        
        if self.request.user.is_authenticated:
            context['fav'] = Favorite.objects.filter(item=self.get_object(), user=self.request.user)
        else:
            pass
        context['form'] = CommentForm()
        return context
  
            
        
    


class ItemDetailView_s(LoginRequiredMixin, DetailView):
    model=item
    template_name = "product_s.html"


class ItemUpdate(UpdateView):

    model=item
    fields=['size_s','size_m','size_l','size_xl','size_xxl', 'name', 'number', 'dis_price', 'price', 'bloglink']
    template_name='update.html'
    
    def get_object(self, *args, **kwargs):
        obj = super(ItemUpdate, self).get_object(*args, **kwargs)
        if not obj.username == self.request.user.username:
            raise Http404
        return obj

@login_required(login_url='/accounts/login')
def post_add(request):
        if (request.user.profile.type == "shop" or request.user.profile.type == "blog"):
            username = request.user.username
            account_obj = Profile.objects.all()
            user=request.user.profile
            link1=""
            link2=""
            form = AddBlog()
            if request.method == 'POST':
                form = AddBlog(request.POST, request.FILES)
                if form.is_valid():
                    obj=form.save(commit=False)
                    if (request.user.profile.type == "shop" or request.user.profile.type == "blog"):
                        obj.user= user
                        obj.username = user.username
                        obj.save()
                                
                        return redirect ('/add_post')
    
    
    
    
            context={'form':form}
    
            return render(request, 'addblog.html', context)
        else:
            return HttpResponse('error you are not authorized to access following page')





class userview(ListView):
        model = User

        def get(self, request, user):
            auth = request.user
            if request.user.is_authenticated:
                get_auth = BlogPost.objects.filter(user=auth.profile, username=user).order_by('-date')
                get_item = BlogPost.objects.filter(~Q(user=auth.profile), username=user).order_by('-date')
                get_user = Profile.objects.filter(username=user)
                object_list = {'get_item':get_item, 'blogger':get_user, 'get_auth':get_auth}
            else:
                get_item = BlogPost.objects.filter(username=user).order_by('-date')
                get_user = Profile.objects.filter(username=user)
                object_list = {'get_item':get_item, 'blogger':get_user}
                
            return render(request, 'blogprofile.html', object_list )




def delete_view(request):
    # object = item.objects.all()
    username = request.user.username
    if request.method == 'POST':
        id = request.POST['delete_id']

        object_list = item.objects.filter(auto_id = id, username = username)

        if object_list:
            object_list.delete()
            
        else:
            return HttpResponse('error you are not authorized to remove following object')

    return redirect('/view_data')


class view_data(LoginRequiredMixin, ListView):
    model = item
    queryset = item.objects.order_by('-date')
    paginate_by=2
    template_name = "index3.html"
    
    def get_queryset(self):
        user=self.request.user.username
        return  item.objects.filter(username = user).order_by('-date')
 

    def get_context_data(self, **kwargs):
        context = super(view_data, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context ['list'] = list
        context ['lists'] = lists
        return context


@login_required(login_url='/accounts/login')
def data(request):
    if (request.user.profile.type == "shop"):

        add_des=""
        dis_price=None
        image2=None
        image3=None
        blog_link=None
    
    
        # if request.user.is_authenticated():
        username = request.user.username
        user = request.user.profile
        account_obj = Profile.objects.all()
        if request.method == 'POST':
            name= request.POST['name']
            image= request.FILES['image']
            image1= request.FILES['image1']
            categories = request.POST['major']
            subcategories = request.POST['minor']
           
    
            price = request.POST['price']
            des=request.POST['description']
            disprice = request.POST['dis_price']
            add_des=request.POST['add_description']
            quantity = request.POST['Quantity']
            size=request.POST.getlist('size')
    
    
            add_img=request.POST.getlist('addimage')
    
            if (categories=="Mens"):
                categories = 'Men'
            elif (categories=="Womens"):
                categories = 'Women'
    
    
            for i in add_img:
    
                if (i=="img"):
                    image2=request.FILES['image2']
                    image3=request.FILES['image3']
                    img2=Image.open(image2)
                    if (img2.format=="JPEG" or img2.format=="PNG"):
                        pass
                    else:
                        return HttpResponse('<strong> Please make sure that uploaded image is JPG or PNG </strong> ')
    
                    img3=Image.open(image3)
                    if (img3.format=="JPEG" or img3.format=="PNG"):
                        pass
                    else:
                        return HttpResponse('<strong> Please make sure that uploaded image is JPG or PNG </strong> ')
    
    
    
                else:
    
                    pass
    
    
    
    
            # img2=request.POST['image2']
            # img3=request.POST['image3']
    
            size_s=""
            size_m=""
            size_l=""
            size_xl=""
            size_xxl=""
            for i in size:
    
                if (i=='S'):
                    size_s='S'
                elif (i=='M'):
                    size_m='M'
                elif (i=='L'):
                    size_l='L'
                elif (i=='XL'):
                    size_xl='XL'
                else:
                    size_xxl='XXL'
    
    
    
    
    
    
    
            if disprice:
                dis_price=disprice
            img=Image.open(image)
            img1=Image.open(image1)
        
        
            if (img.format=="JPEG" or img.format=="PNG" ):
                pass
            else:
                return HttpResponse('<strong> Please1 make sure that uploaded image is JPG or PNG </strong>')
            if (img1.format=="JPEG" or img1.format=="PNG"):
                pass
            else:
                return HttpResponse('<strong> Please make sure that uploaded image is JPG or PNG </strong>')
        
        
        
            new = item(user=user, name=name, title=name, image=image, username=username, category=categories, subcategory=subcategories, price=price, description=des, dis_price=dis_price,
                        add_description=add_des,bloglink=blog_link, number=quantity, image1=image1, image2=image2, image3=image3, size_s=size_s, size_m=size_m, size_l=size_l, size_xl=size_xl, size_xxl=size_xxl )
            new.save()
                        
        
            return redirect ('/data')
                    
        return render (request, 'conform.html')
    else:
        return HttpResponse('error you are not authorized to access following page')
        






@login_required(login_url='/account/login')
def welcome(request):
    user=request.user.username
    type=request.user.profile.type
    if type == "shop":
        context={'user':user,'shop':'shop'}
        return render(request, 'welcome.html', context)
    
    else:
        context={'user':user}
        return render(request, 'welcome.html', context)
        

    
            

    




class Menfilter(ListView):
    model = item
    paginate_by=2
    template_name = "index.html"
    
    
    
    def get_queryset(self):
        Menlist = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop']
        i=self.kwargs['name']
        if i in Menlist:
            return  item.objects.filter(category = "Men", subcategory=self.kwargs['name']).order_by('-date')

            
            

            
    def get_context_data(self, **kwargs):
        context = super(Menfilter, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['Men']  = CImage.objects.filter(Category="Men")
        context['Women']  = CImage.objects.filter(Category="Women")
        context['Kids']  = CImage.objects.filter(Category="Kids")
        context['carouselo'] = IndexCarousel.objects.filter(Category="Men")[:1]
        context['carousel'] = IndexCarousel.objects.filter(Category="Men")[1:]
        context['list'] = list
        context['lists'] = lists
        return context
     
            
                
       
        







class Womenfilter(ListView):
    model = item
    paginate_by=2
    template_name = "index.html"

    def get_queryset(self):
        Womenlist=['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Goldstar','Canvas','Sports','Kurtha','Saree','Skirts_Pants',
        'Dresses','Heels','Boots','CloseShoe','Sandals']
        i=self.kwargs['name']
        if i in Womenlist:
            return  item.objects.filter(category = "Women", subcategory=self.kwargs['name']).order_by('-date')
            
    def get_context_data(self, **kwargs):
        context = super(Womenfilter, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['Men']  = CImage.objects.filter(Category="Men")
        context['Women']  = CImage.objects.filter(Category="Women")
        context['Kids']  = CImage.objects.filter(Category="Kids")
        context['carouselo'] = IndexCarousel.objects.filter(Category="Women")[:1]
        context['carousel'] = IndexCarousel.objects.filter(Category="Women")[1:]
        context['list'] = list
        context['lists'] = lists
        return context


class Kidfilter(ListView):
    allow_empty = True
    model = item
    paginate_by=2
    template_name = "index.html"

        # try:
        #     return super().dispatch(*args, **kwargs)
        # except Http404:
        #     return redirect('/')
            
    def get_queryset(self):
        Kidlist=['ClothingB','ClothingG','FootwearsB','FootwearsG']
        i=self.kwargs['name']
        if i in Kidlist:
            return  item.objects.filter(category = "Kids", subcategory=self.kwargs['name']).order_by('-date')
        
        
            
    def get_context_data(self, **kwargs):
        context = super(Kidfilter, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['Men']  = CImage.objects.filter(Category="Men")
        context['Women']  = CImage.objects.filter(Category="Women")
        context['Kids']  = CImage.objects.filter(Category="Kids")
        context['carouselo'] = IndexCarousel.objects.filter(Category="Kids")[:1]
        context['carousel'] = IndexCarousel.objects.filter(Category="Kids")[1:]
        context['list'] = list
        context['lists'] = lists
        return context
    
  
        
        
class Menfilter_s(ListView):
    model = item
    paginate_by=2
    template_name = "index3.html"
    

    def get_queryset(self):
        user=self.request.user.username
        Menlist = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop']
        i=self.kwargs['name']
        if i in Menlist:
            return  item.objects.filter(category = "Men", username=user, subcategory=self.kwargs['name']).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super(Menfilter_s, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['list'] = list
        context['lists'] = lists
        return context

class Womenfilter_s(ListView):
    model = item
    paginate_by=2
    template_name = "index3.html"

    def get_queryset(self):
        user=self.request.user.username
        Womenlist=['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Goldstar','Canvas','Sports','Kurtha','Saree','Skirts_Pants',
        'Dresses','Heels','Boots','CloseShoe','Sandals']
        i=self.kwargs['name']
        if i in Womenlist:
            return  item.objects.filter(category = "Women", username=user, subcategory=self.kwargs['name']).order_by('-date')
        
    def get_context_data(self, **kwargs):
        context = super(Womenfilter_s, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['list'] = list
        context['lists'] = lists
        return context


class Kidfilter_s(ListView):
    model = item
    paginate_by=2
    template_name = "index3.html"
    

    def get_queryset(self):
        
        user=self.request.user.username
        Kidlist=['ClothingB','ClothingG','FootwearsB','FootwearsG']
        i=self.kwargs['name']
        if i in Kidlist:
            return  item.objects.filter(category = "Kids", username=user, subcategory=self.kwargs['name']).order_by('-date')
        
    def get_context_data(self, **kwargs):
        context = super(Kidfilter_s, self).get_context_data(**kwargs)
        list = ['Tops_Tshirt','Hoodies_Sweatshirt','Jacket_Gilets','Jeans','Joggers',
        'Shorts','Leathers','BagPacks','Accessories','Kurtha','Saree','Skirts_Pants',
        'Dresses','ClothingB','ClothingG']
        lists = ['Goldstar','Canvas','Sports','Formals','Football','Basketball','Sandal_Flipflop','Heels','Boots','CloseShoe','Sandals','FootwearsB','FootwearsG']
        context['list'] = list
        context['lists'] = lists
        return context


@login_required(login_url='/accounts/login')
def add_comment(request, slug):
    form = CommentForm(request.POST)
    if request.method == "POST":
        if request.user.is_authenticated:
            if form.is_valid():
                name = form.cleaned_data['name']
                obj = get_object_or_404(item, slug=slug)
                user = request.user.profile
                email = form.cleaned_data ['email']
                message = form.cleaned_data ['message']
                comment =Comment(Name=name, Object=obj, User=user, Email=email, Message=message)
                comment.save()
                
                #email section
                
                # html_file = get_template('mail_template.html')
                # obj_d = { 'obj':obj}
                # html_content = html_file.render(obj_d)
                # sub = 'Comment'
                # from_email = 'noreply@luumania.com'
                # mail = obj.user.user.email
                # to_email = [mail, ]
                # msg = EmailMultiAlternatives(subject=sub, from_email=from_email, to=to_email)
                # msg.attach_alternative(html_content, 'text/html')
                # msg.send()
                
                
                
                
                
                    
                return redirect("content:productdetail", slug=slug)
            else:
                return redirect("content:productdetail", slug=slug)
            
        else:
            return redirect('/accounts/login')

    

def del_comment(request, id, slug):
    get_item = get_object_or_404(Comment, id=id)
    get_user = request.user.profile
    user = request.user
    if user.is_authenticated:
        if get_item.User == get_user:
            get_item.delete()
            return redirect("content:productdetail", slug=slug)
        else:
            return HttpResponse('You are not authorized to delete following object.')


def del_blog(request, slug):
    get_item = get_object_or_404(BlogPost, slug=slug)
    get_user = request.user.profile
    user = request.user
    if user.is_authenticated:
        if get_item.user == get_user:
            get_item.delete()
            return redirect("/blog")
        else:
            return HttpResponse('You are not authorized to delete following object.')
