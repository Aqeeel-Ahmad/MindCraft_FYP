from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# main/urls.py
# from main import views, user_login



urlpatterns = [
    path('', views.home, name='home'),
    path('base', views.base, name='base'), 
    path('404', views.page_not_found , name='404'),
    path('courses', views.single_course, name='single_course'),
    path('courses/filter-data', views.filter_data, name = 'filter-data'),
    path('course/<slug:slug>', views.course_details, name='course_details'),
    path('search', views.search_course, name='search_course'),
    
    path('contact', views.contact_us, name='contact_us'),
    path('about', views.about_us, name='about_us'),
    
    path('accounts/register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('profile/', views.profile, name='profile'),
    path('enrolled-courses/', views.enrolled_courses, name='enrolled_courses'),
    # path('logout/', views.logout_view, name='logout'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    
    path('accounts/update_profile',views.update_profile, name='update_profile'), #profile
    path('accounts/update_profile/updated_profile',views.updated_profile, name='updated_profile'),   #update_profile
    path('checkout/<slug:slug>', views.checkout, name = 'checkout'),
    path('my_courses', views.my_courses, name = 'my_courses'),
    path('verify_payment', views.verify_payment, name='verify_payment'),
    path('payment-cancel/', views.cancel_payment, name='payment_cancel'),
    path('save-order/', views.save_order, name='save_order'), 
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
