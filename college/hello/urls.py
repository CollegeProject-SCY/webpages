from django.conf.urls import handler404
from django.urls import path
from django.urls.resolvers import URLPattern
from django.contrib.auth import views as auth_views

from . import views
import hello



urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register, name="register"),
    path('loged_in/',views.loged_in, name="loged_in"),
    path('log_in',views.log_in, name="log_in"),
    path('generate/pass_val',views.pass_val, name="pass_val"),
    path('renewal/renewal_auth',views.renewal_auth, name="renewal_auth"),
    path('contact_us/contact_form',views.contact_form, name="contact_form"),
    path('apply/apply_form',views.apply_form, name="apply_form"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('apply/',views.apply, name="apply"),
    path('view/',views.view, name="view"),
    path('about_us/',views.about_us, name="about_us"),
    path('contact_us/',views.contact_us, name="contact_us"),
    path('payment/',views.payment, name="payment"),
    path('renewal/',views.renewal, name="renewal"),
    path('generate/',views.generate, name="generate"),
    path('log_out',views.log_out, name="log_out"),
    path('renewal/renewal_fun',views.renewal_fun, name="renewal_fun"),

    

]
