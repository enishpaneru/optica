from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import BookGlassForm,AddGlassForm,UserCreateForm,AddBrandForm,BuyGlassForm,UserinfoChangeForm,SignupForm
from .models import Glass, Brand, GlassInstance,booking,Order,OrderDetail,UserDetail
from .tokens import account_activation_token
from notifications.signals import notify


class Main():
    def index(request):
        """
        View function for home page of site.
        """
        glass=get_object_or_404(Glass,pk=23)

        return render(
            request,
            'index.html',

        )

    @user_passes_test(lambda u: u.is_superuser)
    def ownerview(request):
        """
        View function for home page of site.
        """


        return render(
            request,
            'indexowner.html'

        )

    def about(request):
        """
        View function for home page of site.
        """

        return render(
            request,
            'about.html'

        )

class ListViewUser():
    def GlassListView(request):
        page = request.GET.get('page', 1)
        search =request.GET.get('searchvalue',None)

        if "search" in request.GET or search != None:
            if search != None:
                searchval = search
            else:
                searchval=request.GET['search']

            glasslist= Glass.objects.filter(Q(name__icontains=searchval)|Q(brand__name__icontains=searchval))
            paginator = Paginator(glasslist,8)
            try:
                glass_list = paginator.page(page)
            except PageNotAnInteger:
                glass_list = paginator.page(1)
            except EmptyPage:
                glass_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/glass_list.html', {'glass_list': glass_list,'searchvalue':request.GET["search"]})

        else:

            glasslist= Glass.objects.all()
            paginator = Paginator(glasslist,8)

            try:
                glass_list = paginator.page(page)
            except PageNotAnInteger:
                glass_list = paginator.page(1)
            except EmptyPage:
                glass_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/glass_list.html', {'glass_list': glass_list})

    def BrandListView(request):
        page = request.GET.get('page',1)
        if "search" in request.GET:

            brandlist= Brand.objects.filter(name__icontains=request.GET["search"])
            paginator = Paginator(brandlist,8)
            try:
                brand_list = paginator.page(page)
            except PageNotAnInteger:
                brand_list = paginator.page(1)
            except EmptyPage:
                brand_list = paginator.page(paginator.num_pages)

        else:
            brandlist= Brand.objects.all()
            paginator = Paginator(brandlist,8)
            try:
                brand_list = paginator.page(page)
            except PageNotAnInteger:
                brand_list = paginator.page(1)
            except EmptyPage:
                brand_list = paginator.page(paginator.num_pages)

        return render(request, 'catalog/brand_list.html', {'brand_list': brand_list})

    @login_required
    def LoanedGlassesByUserListView(request):
        """
        Generic class-based view listing books on loan to current user.
        """
        a=500000
        allglass=booking.objects.all()
        for gl in allglass:
            if gl.user == request.user:
                a=a-gl.glass.price*gl.booknovalue
        glass=Glass.objects.filter(booker=request.user)
        Bookno=booking.objects.filter(user=request.user)
        return render(request, 'catalog/glassinstance_list_borrowed_user.html', context={'glass_list':glass,'Book_list':Bookno,'remain':a})
    @login_required
    def OrderListViewuser(request):

        page = request.GET.get('page', 1)
        orderlist=Order.objects.filter(user=request.user).order_by('-active','orderdate')
        paginator = Paginator(orderlist,8)
        return render(request,'catalog/order_listuser.html',{'order_list':orderlist})
    @login_required
    def OrderDetailListViewuser(request,pk):
        orderuser=get_object_or_404(Order,pk =pk)
        page = request.GET.get('page', 1)
        orderdetaillist=OrderDetail.objects.filter(orderuser=orderuser)
        paginator = Paginator(orderdetaillist,8)

        return render(request, 'catalog/orderdetail_listuser.html', {'orderdetail_list': orderdetaillist})

class ListViewOwner():
    @user_passes_test(lambda u: u.is_superuser)
    def GlassListViewowner(request):
        page = request.GET.get('page', 1)


        if "search" in request.GET:

            glasslist= Glass.objects.filter(Q(name__icontains=request.GET["search"])|Q(brand__name__icontains=request.GET["search"]))
            paginator = Paginator(glasslist,8)
            try:
                glass_list = paginator.page(page)
            except PageNotAnInteger:
                glass_list = paginator.page(1)
            except EmptyPage:
                glass_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/glass_list_owner.html', {'glass_list': glass_list,'searchvalue':request.GET["search"]})

        else:

            glasslist= Glass.objects.all()
            paginator = Paginator(glasslist,8)

            try:
                glass_list = paginator.page(page)
            except PageNotAnInteger:
                glass_list = paginator.page(1)
            except EmptyPage:
                glass_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/glass_list_owner.html', {'glass_list': glass_list})

    @user_passes_test(lambda u: u.is_superuser)
    def BrandListViewowner(request):
        page = request.GET.get('page',1)
        if "search" in request.GET:

            brandlist= Brand.objects.filter(name__icontains=request.GET["search"])
            paginator = Paginator(brandlist,8)
            try:
                brand_list = paginator.page(page)
            except PageNotAnInteger:
                brand_list = paginator.page(1)
            except EmptyPage:
                brand_list = paginator.page(paginator.num_pages)

        else:
            brandlist= Brand.objects.all()
            paginator = Paginator(brandlist,8)
            try:
                brand_list = paginator.page(page)
            except PageNotAnInteger:
                brand_list = paginator.page(1)
            except EmptyPage:
                brand_list = paginator.page(paginator.num_pages)

        return render(request, 'catalog/brand_list_owner.html', {'brand_list': brand_list})

    @user_passes_test(lambda u: u.is_superuser)
    def UsersListViewowner(request):
        page = request.GET.get('page',1)
        if "search" in request.GET:

            userlist= User.objects.filter(name__icontains=request.GET["search"])
            paginator = Paginator(userlist,8)
            try:
                user_list = paginator.page(page)
            except PageNotAnInteger:
                user_list = paginator.page(1)
            except EmptyPage:
                user_list = paginator.page(paginator.num_pages)

        else:
            userlist= User.objects.all()
            paginator = Paginator(userlist,8)
            try:
                user_list = paginator.page(page)
            except PageNotAnInteger:
                user_list = paginator.page(1)
            except EmptyPage:
                user_list = paginator.page(paginator.num_pages)

        return render(request, 'catalog/user_list_owner.html', {'user_list': user_list})
    @user_passes_test(lambda u: u.is_superuser)
    def bookingListViewowner(request):
        page = request.GET.get('page', 1)


        if "search" in request.GET:

            bookinglist= booking.objects.filter(Q(name__icontains=request.GET["search"])|Q(brand__name__icontains=request.GET["search"]))
            paginator = Paginator(bookinglist,8)
            try:
                booking_list = paginator.page(page)
            except PageNotAnInteger:
                booking_list = paginator.page(1)
            except EmptyPage:
                booking_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/booking_list.html', {'booking_list': booking_list,'searchvalue':request.GET["search"]})

        else:

            bookinglist= booking.objects.all().order_by('bookdate')
            paginator = Paginator(bookinglist,8)

            try:
                booking_list = paginator.page(page)
            except PageNotAnInteger:
                booking_list = paginator.page(1)
            except EmptyPage:
                booking_list = paginator.page(paginator.num_pages)
            return render(request, 'catalog/booking_list.html', {'booking_list': booking_list})
    @user_passes_test(lambda u: u.is_superuser)
    def OrderListViewowner(request,obj):
        if obj=="active":
            page = request.GET.get('page', 1)
            orderlist=Order.objects.filter(active=True).order_by('orderdate')
            paginator = Paginator(orderlist,8)
        if obj=="notactive":
            page = request.GET.get('page', 1)
            orderlist=Order.objects.filter(active=False).order_by('orderdate')
            paginator = Paginator(orderlist,8)

        return render(request, 'catalog/order_listowner.html', {'order_list': orderlist})
    @user_passes_test(lambda u: u.is_superuser)
    def OrderDetailListViewowner(request,pk):
        orderuser=get_object_or_404(Order,pk =pk)
        page = request.GET.get('page', 1)
        orderdetaillist=OrderDetail.objects.filter(orderuser=orderuser)
        paginator = Paginator(orderdetaillist,8)

        return render(request, 'catalog/orderdetail_listowner.html', {'orderdetail_list': orderdetaillist})

class DetailViewUser():
    class GlassDetailView(generic.DetailView):
        model = Glass

    def BrandDetailView(request,pk):
        page = request.GET.get('page',1)
        brand =Brand.objects.get(pk=pk)

        glasslist= brand.glass_set.all()
        paginator = Paginator(glasslist,8)
        glass_list = paginator.page(page)

        return render(request, 'catalog/brand_detail.html', {'brand':brand,'glass_list': glass_list})

class DetailViewOwner():
    class GlassDetailownerView(SuperuserRequiredMixin,generic.DetailView):
            model = Glass
            template_name = 'catalog/glass_detailowner.html'

    class UserDetailownerView(SuperuserRequiredMixin,generic.DetailView):
        model = User
        template_name = 'catalog/user_detailowner.html'

    @user_passes_test(lambda u: u.is_superuser)
    def BrandDetailOwnerView(request,pk):
        page = request.GET.get('page',1)
        brand =Brand.objects.get(pk=pk)
        glasslist= brand.glass_set.all()
        paginator = Paginator(glasslist,8)
        glass_list = paginator.page(page)

        return render(request, 'catalog/brand_detailowner.html', {'brand':brand,'glass_list': glass_list})
    @user_passes_test(lambda u: u.is_superuser)
    def bookingDetailOwnerView(request,pk):
        bookings =booking.objects.get(pk=pk)


        return render(request, 'catalog/booking_detail.html', {'booking':bookings})

class userprofile():
    @login_required
    def mycart(request):
        """
        Generic class-based view listing books on loan to current user.
        """
        total=request.session.get('total',0)
        cart=request.session.get('cart',{})
        displist={}

        for glassid in cart:
            glass=get_object_or_404(Glass, pk = glassid)
            displist[glass]=cart[glassid]

        return render(request, 'catalog/mycart.html', context={'disp_list':displist,'total':total})

    @login_required
    def myprofile(request):
        """
        Generic class-based view listing books on loan to current user.
        """
        user= request.user
        notcount = user.notifications.unread().count
        print (notcount)
        return render(request, 'catalog/myprofile.html', context={'user':user,'notcount':notcount})
    @login_required
    def shownotifications(request):
        """
        Generic class-based view listing books on loan to current user.
        """
        user= request.user
        delete=request.GET.get('clear',None)
        readmark=request.GET.get('read',None)
        if readmark == "True":
            user.notifications.mark_all_as_read()
        if delete == "True":
            print (delete)
            for notice in user.notifications.all():
                notice.delete()

        notread = user.notifications.unread()
        read=user.notifications.read()

        return render(request, 'catalog/notifications.html', context={'user':user,'notread':notread,'read':read})
class UserAction():
    @login_required
    def userinfochange(request):
        """
        View function for renewing a specific BookInstance by librarian
        """
        user=request.user
        m1=UserDetail.objects.get(user=user)
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = UserinfoChangeForm(request.POST,user=user)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

                user.username=form.cleaned_data['username']
                user.first_name=form.cleaned_data['first_name']
                user.last_name=form.cleaned_data['last_name']
                user.email=form.cleaned_data['email']
                user.save()

                m1.location = form.cleaned_data['location']
                m1.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('my-profile') )

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_number = 3
            form = UserinfoChangeForm(initial={'username': user.username,'first_name': user.first_name,'last_name': user.last_name,'email': user.email,'location': m1.location,},user=user)

        return render(request, 'catalog/change_user_info.html', {'form': form})

    @login_required
    def book_a_glass(request, pk):
        """
        View function for renewing a specific BookInstance by librarian
        """
        glass=get_object_or_404(Glass, pk = pk)
        allglass=booking.objects.all()
        a=500000
        b=1

        for gl in allglass:
            if gl.user == request.user:
                a=a-gl.glass.price*gl.booknovalue
            if gl.user == request.user and gl.glass==glass:
                b=0





        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = BookGlassForm(request.POST,pk =pk,remain=a)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

                m1 = booking(id=pk+str(request.user.id),user=request.user,glass=glass,booknovalue=form.cleaned_data['Bookno'],bookdate=datetime.date.today())
                m1.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('my-booked') )

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_number = 3
            form = BookGlassForm(initial={'Bookno': proposed_number},pk=pk,remain=a)

        return render(request, 'catalog/book_a_glass.html', {'form': form, 'glass':glass,'prebook':b})

    @login_required
    def buy_a_glass(request, pk):
        """
        View function for renewing a specific BookInstance by librarian
        """
        total=request.session.get('total',0)
        cart=request.session.get('cart',{})
        glass=get_object_or_404(Glass, pk = pk)



            # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = BuyGlassForm(request.POST)

            # Check if the form is valid:
            if form.is_valid():
                cart[glass.id]=form.cleaned_data['Buyno']
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                total=total+glass.price*cart[glass.id]
                request.session['cart']=cart
                request.session['total']=total


                # redirect to a new URL:
                return HttpResponseRedirect(reverse('my-cart') )

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_number = 1
            form = BuyGlassForm(initial={'Buyno': proposed_number})

        return render(request, 'catalog/buy_a_glass.html', {'form': form, 'glass':glass})

    @login_required
    def completeorder(request):
        cart=request.session.get("cart",{})
        total=request.session.get('total',0)
        m1=Order(user=request.user,orderdate=datetime.date.today(),active=True,amount=total)
        m1.save()
        for glassid in cart:
            currentglass=get_object_or_404(Glass,pk=glassid)
            m2=OrderDetail(glass=currentglass,orderno=cart[glassid],orderuser=m1)
            m2.save()
        del request.session['cart']
        del request.session['total']
        return HttpResponseRedirect(reverse('my-ordered') )

    @login_required
    def confirmorder(request):


        return render(request,'catalog/orderconfirm.html',)
    @login_required
    def delcart(request,pk):
        total=request.session.get('total',0)
        cart=request.session.get('cart',{})
        glass=get_object_or_404(Glass, pk = pk)
        newlist=[]
        print (cart)
        print(glass.id)
        for key in cart.copy():
            if int(glass.id) == int(key):
                total=total-glass.price*cart[key]
                del cart[key]
                print("delete success")
                print (cart)
                newcart=cart
        request.session['cart']=newcart
        request.session['total']=total
        return HttpResponseRedirect(reverse('my-cart') )
class OwnerAction():

    @user_passes_test(lambda u: u.is_superuser)
    def deleteobject(request,pk,obj):
        if obj == 'glass':
            delobj=get_object_or_404(Glass,pk=pk)
        if obj == 'brand':
            delobj=get_object_or_404(Brand,pk=pk)
        if obj == 'booking':
            delobj=get_object_or_404(booking,pk=pk)
            delobj.delete()
            return HttpResponseRedirect(reverse('bookings') )
        if obj == 'order':
            delobj=get_object_or_404(Order,pk=pk)
            delobj.delete()
            return HttpResponseRedirect(reverse('ordersowner') )
        delobj.delete()

        return HttpResponseRedirect(reverse('owner') )

    @user_passes_test(lambda u: u.is_superuser)
    def GlassAdd(request):
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = AddGlassForm(request.POST,request.FILES)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

                m1 = Glass(name=form.cleaned_data['name'],price=form.cleaned_data['price'],brand=form.cleaned_data['brand'],detail=form.cleaned_data['detail'],glass_pic=request.FILES['glass_pic'],)
                m1.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('index') )

        # If this is a GET (or any other method) create the default form.
        else:

            form = AddGlassForm(initial={'name': "",'detail':""})

        return render(request, 'catalog/add_a_glass.html', {'form': form})

    @user_passes_test(lambda u: u.is_superuser)
    def BrandAdd(request):
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = AddBrandForm(request.POST,request.FILES)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

                m1 = Brand(name=form.cleaned_data['name'],detail=form.cleaned_data['detail'],brand_pic=request.FILES['brand_pic'],)
                m1.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('index') )

        # If this is a GET (or any other method) create the default form.
        else:

            form = AddBrandForm(initial={'name': "",'detail':""})

        return render(request, 'catalog/add_a_brand.html', {'form': form})

    @user_passes_test(lambda u: u.is_superuser)
    def GlassEdit(request,pk):
        m1=get_object_or_404(Glass,pk=pk)
            # If this is a POST request then process the Form data
        if request.method == 'POST':

                # Create a form instance and populate it with data from the request (binding):
            form = AddGlassForm(request.POST,request.FILES)

                # Check if the form is valid:
            if form.is_valid():
                    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

                m1.name = form.cleaned_data['name']
                m1.price=form.cleaned_data['price']
                m1.brand=form.cleaned_data['brand']
                m1.detail=form.cleaned_data['detail']
                m1.glass_pic=request.FILES['glass_pic']
                m1.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('index') )

            # If this is a GET (or any other method) create the default form.
        else:
            form = AddGlassForm(initial={'name': m1.name,'detail':m1.detail,'price':m1.price,'brand':m1.brand,'glass_pic':m1.glass_pic})

        return render(request, 'catalog/add_a_glass.html', {'form': form})

    @user_passes_test(lambda u: u.is_superuser)
    def BrandEdit(request,pk):
        m1=get_object_or_404(Brand,pk=pk)
            # If this is a POST request then process the Form data
        if request.method == 'POST':
                # Create a form instance and populate it with data from the request (binding):
            form = AddGlassForm(request.POST,request.FILES)

                # Check if the form is valid:
            if form.is_valid():
                    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                m1.name = form.cleaned_data['name']
                m1.price=form.cleaned_data['price']
                m1.brand=form.cleaned_data['brand']
                m1.detail=form.cleaned_data['detail']
                m1.glass_pic=request.FILES['glass_pic']
                m1.save()
                    # redirect to a new URL:
                return HttpResponseRedirect(reverse('index') )

            # If this is a GET (or any other method) create the default form.
        else:
            form = AddGlassForm(initial={'name': m1.name,'detail':m1.detail,'price':m1.price,'brand':m1.brand,'glass_pic':m1.glass_pic})

        return render(request, 'catalog/add_a_glass.html', {'form': form})

    class UserCreate(SuperuserRequiredMixin,CreateView):
        model = User
        template_name='catalog/user_form.html'
        form_class = UserCreateForm
        success_url = reverse_lazy('users')

    class UserUpdate(SuperuserRequiredMixin,UpdateView):
        model = User
        fields = ['first_name','last_name','username','is_superuser']
        template_name='catalog/user_formchange.html'
        success_url = reverse_lazy('users')

    class UserDelete(SuperuserRequiredMixin,DeleteView):
        model = User
        template_name='catalog/user_confirm_delete.html'
        success_url = reverse_lazy('users')
    @user_passes_test(lambda u: u.is_superuser)
    def ordercomplete(request,pk):
        order=get_object_or_404(Order,pk=pk)
            # If this is a POST request then process the Form data
        order.active=False
        order.save()
        notify.send(order, recipient=order.user, verb='your order has been marked as completed.If you have not received goods, please contact the store. Your order no. is:')
        return HttpResponseRedirect(reverse('ordersowner',kwargs={'obj':"active"}) )
class extra():
    def signup(request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)

                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user':user, 'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                # user.email_user(subject, message)
                toemail = form.cleaned_data.get('email')
                email = EmailMessage(subject, message, to=[toemail])
                email.send()
                return render(request, 'catalog/checkemail.html', {'form': form})
        else:
            form = SignupForm()
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
            m1=UserDetail(user=user)
            m1.save()
            login(request, user)
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
