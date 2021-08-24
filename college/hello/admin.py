from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.base import Model
from django.core.mail import send_mail
from django.http import request

#Register your models here.
from hello.models import Account,applicants,Route,pass_rate,contact_list


class accAdmin(admin.AdminSite):
    site_header='Admin Area'
    

class AccntAdmin(admin.ModelAdmin):
    list_display=('email','username','phone','is_active','pass_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return False

ac_site=accAdmin(name='Administration')
ac_site.register(Account,AccntAdmin)


def email_pass(self, request, queryset):
        mail_cont='Dear applicant,your application for bus pass has been Approved. Login and visit payment Section  to pay the fees and then generate your pass'
        for i in queryset:
            if i.mail_send==False:
                send_mail('Application Approved', mail_cont ,'roadwayexpressscy@gmail.com' , [i.email], fail_silently=False)
                queryset.update(mail_send=True)         

        email_pass.short_description = "Send an email to approved applicants"

    

class Accntuser(admin.ModelAdmin):
    #user_pass=request.user.pass_id
    #approval=applicants.objects.get(pass_id=user_pass).approval
    model=applicants
    list_display=('student_name','rd_number','course','adhar_number','pass_id','mail_send','approval')
    actions=[email_pass]
    def has_add_permission(self, request):
        return False
    
    readonly_fields = ('passport_size_image','college_fees_image','adhar_image','study_certificate_image','previous_marks_image','terms_cond',)
   


ac_site.register(applicants,Accntuser) 

class add_route(admin.ModelAdmin):
    list_display=('From_place','To_place','Timings','Bus_Number')

ac_site.register(Route,add_route)

class pass_amt(admin.ModelAdmin):
    list_display=('category','pass_price','processing_fee')

ac_site.register(pass_rate,pass_amt)

class contact_form(admin.ModelAdmin):
    list_display=('username','email','phone','messages')
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return False

ac_site.register(contact_list,contact_form)
