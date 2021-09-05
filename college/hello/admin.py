
from os import truncate
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.base import Model
from django.core.mail import send_mail
from django.http import request

#Register your models here.

from hello.models import Account,applicants,Route,pass_rate,contact_list,depos,Transaction


class accAdmin(admin.AdminSite):
    site_header='Admin Area'
    

class AccntAdmin(admin.ModelAdmin):
    list_display=('email','username','phone','is_active','pass_id')
    list_filter = ('date_joined', )
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return False
    
ac_site=accAdmin(name='Administration')
ac_site.register(Account,AccntAdmin)


def application_approval(self, request, queryset):
        mail_cont='Dear applicant,your application for bus pass has been Approved. Login and visit payment Section  to pay the fees and then generate your pass'
        for i in queryset:
            if i.approval==False:
                send_mail('Application Approved', mail_cont ,'roadwayexpressscy@gmail.com' , [i.email], fail_silently=False)
                queryset.update(mail_send=True)         
                queryset.update(approval=True)
               
                if i.caste=='SC' or i.caste=='ST':
                    queryset.update(bus_amount=200)
                elif i.caste=='OBC':
                    queryset.update(bus_amount=1400)
                else:
                    queryset.update(bus_amount=1400)
                
        application_approval.short_description = "Application Approval"

    

class Accntuser(admin.ModelAdmin):
    #user_pass=request.user.pass_id
    #approval=applicants.objects.get(pass_id=user_pass).approval
    model=applicants
    list_display=('student_name','rd_number','course','adhar_number','pass_id','mail_send','approval')
    actions=[application_approval]
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request,obj=None):
       return True
    
    #readonly_fields = ('passport_size_image','college_fees_image','adhar_image','study_certificate_image','previous_marks_image','terms_cond',)
   


ac_site.register(applicants,Accntuser) 

class add_route(admin.ModelAdmin):
    list_display=('From_place','To_place','Timings','Bus_Number')

ac_site.register(Route,add_route)

class pass_amt(admin.ModelAdmin):
    list_display=('category','pass_price','processing_fee')

ac_site.register(pass_rate,pass_amt)

class depos_add(admin.ModelAdmin):
    list_display=('city','bus_photo','address')

ac_site.register(depos,depos_add)

class contact_form(admin.ModelAdmin):
    list_display=('username','email','phone','messages')
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return False

ac_site.register(contact_list,contact_form)


class Payment(admin.ModelAdmin):
    list_display=('username','made_on','amount','order_id','status')
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return True

ac_site.register(Transaction,Payment)