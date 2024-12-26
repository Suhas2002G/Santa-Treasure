from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home),
    path('login', views.user_login),
    path('register', views.register),
    path('logout', views.user_logout),
    path('myprofile', views.myprofile),
    path('gifts', views.gifts),
    path('addaddress', views.addaddress),
    path('search', views.search),
    path('giftdetail/<pid>', views.giftdetail),
    path('addtocart/<pid>', views.addtocart),
    path('viewcart', views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('sort/<x>', views.sort),
    path('remove/<cid>',views.remove),
    path('place_order',views.place_order),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),

    path('adminLogin', views.adminLogin),
    path('dashboard', views.dashboard),
    path('trackorder', views.trackorder),
    path('vieworder/<oid>', views.vieworder),
    
    



]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)