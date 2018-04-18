from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
url(r'^$', views.Main.index, name='index'),
url(r'^owner/$', views.Main.ownerview, name='owner'),
url(r'^about$', views.Main.about, name='about'),

url(r'^glasses/$', views.ListViewUser.GlassListView, name='glasses'),
url(r'^brands/$', views.ListViewUser.BrandListView, name='brands'),
url(r'^myglasses/$', views.ListViewUser.LoanedGlassesByUserListView, name='my-booked'),
url(r'^myordered/$', views.ListViewUser.OrderListViewuser, name='my-ordered'),
url(r'^myorderdetails/(?P<pk>\d+)$', views.ListViewUser.OrderDetailListViewuser, name='orderdetailsuser'),

url(r'^owner/glasses/$', views.ListViewOwner.GlassListViewowner, name='glassesowner'),
url(r'^owner/brands/$', views.ListViewOwner.BrandListViewowner, name='brandsowner'),
url(r'^owner/users/$', views.ListViewOwner.UsersListViewowner, name='users'),
url(r'^owner/bookings/$', views.ListViewOwner.bookingListViewowner, name='bookings'),
url(r'^owner/orders/(?P<obj>\w+)$', views.ListViewOwner.OrderListViewowner, name='ordersowner'),
url(r'^owner/orderdetails/(?P<pk>\d+)$', views.ListViewOwner.OrderDetailListViewowner, name='orderdetailsowner'),

url(r'^glass/(?P<pk>\d+)$', views.DetailViewUser.GlassDetailView.as_view(), name='glass-detail'),
url(r'^brand/(?P<pk>\d+)$', views.DetailViewUser.BrandDetailView, name='brand-detail'),

url(r'^owner/glass/(?P<pk>\d+)$', views.DetailViewOwner.GlassDetailownerView.as_view(), name='glass-detail-owner'),
url(r'^owner/user/(?P<pk>\d+)$', views.DetailViewOwner.UserDetailownerView.as_view(), name='user-detail-owner'),
url(r'^owner/brand/(?P<pk>\d+)$', views.DetailViewOwner.BrandDetailOwnerView, name='brand-detail-owner'),
url(r'^owner/booking/(?P<pk>\d+)$', views.DetailViewOwner.bookingDetailOwnerView, name='booking-detail'),


url(r'^mycart/$', views.userprofile.mycart, name='my-cart'),
url(r'^myprofile/$', views.userprofile.myprofile, name='my-profile'),
url(r'^myprofile/notifications/$', views.userprofile.shownotifications, name='shownotifications'),

url(r'^glass/(?P<pk>\d+)/book$', views.UserAction.book_a_glass, name='to-book'),
url(r'^glass/(?P<pk>\d+)/buy$', views.UserAction.buy_a_glass, name='to-buy'),
url(r'^ordercomplete$', views.UserAction.completeorder, name='ordercomplete'),
url(r'^orderconfirm$', views.UserAction.confirmorder, name='orderconfirm'),
url(r'^userinfochange/$', views.UserAction.userinfochange, name='userinfochange'),
url(r'^delcart/(?P<pk>\d+)$', views.UserAction.delcart, name='delcart'),

url(r'^delete/(?P<pk>\d+)/(?P<obj>\w+)$', views.OwnerAction.deleteobject, name='delete-object'),
url(r'^owner/addglass$', views.OwnerAction.GlassAdd, name='addglass'),
url(r'^owner/addBrand$', views.OwnerAction.BrandAdd, name='addbrand'),
url(r'^owner/editglass/(?P<pk>\d+)$', views.OwnerAction.GlassEdit, name='editglass'),
url(r'^user/create/$', views.OwnerAction.UserCreate.as_view(), name='user_create'),
url(r'^user/(?P<pk>\d+)/update/$', views.OwnerAction.UserUpdate.as_view(), name='user_update'),
url(r'^user/(?P<pk>\d+)/delete/$', views.OwnerAction.UserDelete.as_view(), name='user_delete'),
url(r'^order/(?P<pk>\d+)/$', views.OwnerAction.ordercomplete, name='order-complete'),

url(r'^signup/$', views.extra.signup, name='signup'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.extra.activate, name='activate'),
]
