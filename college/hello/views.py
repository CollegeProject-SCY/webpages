from django import template
from django.contrib.auth.models import User
from django.core.mail.message import utf8_charset
from django.http import request, response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.utils import timezone
import random ,string


# Create your views here.

from django.views.decorators.csrf import requires_csrf_token
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import http_date, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from .models import Account, contact_list,applicants,Route,pass_rate
from django.utils.encoding import force_bytes
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.dateparse import parse_date
from django.contrib.admin.models import LogEntry
from datetime import timedelta,date
from django.http import HttpResponse







# Create your views here.
LogEntry.objects.all().delete()
def loged_in(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')
    
@requires_csrf_token
def register(request):
    if request.method =='POST':
         username=request.POST['username']
         email=request.POST['email']
         phone=request.POST['phone']
         password1=request.POST['password']
         encpass=password1+'zzz'
         
         #pass_id=uuid.uuid4()
         if(Account.objects.filter(username=username).exists()):
            messages.info(request, 'username exist :(') 
            return redirect('loged_in') 
              
         elif(Account.objects.filter(email=email).exists()):
            messages.info(request, 'email exist :(') 
            return redirect('loged_in') 
    otp=''.join(random.choice(string.digits) for x in range(4))
    send_mail('OTP', otp ,'yuvarajkharvi4111@gmail.com' , [email], fail_silently=False)
    request.session['username']=username
    request.session['phone']=phone
    request.session['encpass']=encpass
    request.session['email']=email
    request.session['otp']=otp
    return render(request,'otp.html',{'email':email})

    """phone=request.POST['phone']
    password1=request.POST['password']
    encpass=password1+'zzz'
    user_obj =Account.objects.create(username=username, phone=phone, email=email, password=encpass)
    user_obj.set_password(encpass)
    user_obj.save()
    messages.info(request, 'Account Created Successfully :)')  
    print(' user created '+username) 
    return redirect('loged_in')

  """

def verification(request):
    if request.method =='POST':
        first=request.POST['first']
        second=request.POST['second']
        third=request.POST['third']
        fourth=request.POST['fourth']
        user_otp=first+second+third+fourth
        username=request.session['username']
        phone=request.session['phone']
        encpass=request.session['encpass']
        email=request.session['email']
        otp=request.session['otp']
        print(user_otp)
        if user_otp==otp:
            user_obj =Account.objects.create(username=username, phone=phone, email=email, password=encpass)
            user_obj.set_password(encpass)
            user_obj.save()
            messages.info(request, 'Account Created Successfully :)')  
            print(' user created '+username) 
            return redirect('loged_in')
        else:
            return render(request,'otp.html',{'wrong_otp':'wrong_otp'})
        

def log_in(request):  
    if request.method =='POST':
          username=request.POST['username']
          password=request.POST['password']  
          if(Account.objects.filter(username=username).exists()):
                user = Account.objects.get(username=username)
                encpass=password+'zzz'
                if user.check_password(encpass):
                    login(request, user)
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    print('User loged '+username)
                    
                    return redirect('home')
                else:
                   
                    return render(request,'index.html',{'pass':password})

          else:
             
              return render(request,'index.html',{'user_val':username})

    return render(request,'home')
         
def contact_us(request):
    return render(request,'contact.html')

def about_us(request):
    return render(request,'about.html')

@login_required
def apply(request):
    current=float(request.user.pass_id)
    if(current > 0):
        print(current)
        return render(request,'success.html',{'your_already_applied':current})
    else:
        return render(request,'apply.html')

def view(request):
    pass_amts=pass_rate.objects.all()
    dests=Route.objects.all()
    return render(request,'view.html',{'dests':dests, 'pass_amts':pass_amts})

@login_required
def renewal(request):
    try:
        current=request.user.pass_id
        obj=applicants.objects.get(pass_id=current).approval
        if obj:    
            expire_date=applicants.objects.get(pass_id=current).expire_date
            today=date.today()
            if(current == 0):
                return render(request,'success.html',{'your_not_applied_renw':'your_not_applied_renw'})
            else:
                if(today < expire_date):
                    messages.info(request, 'Your pass validity not ended') 
                    return redirect(home)

                else:
                    return render(request,'renewal.html')
        else:
            return render(request,'success.html',{'application_not_approved_renw':'application_not_approved_renw'})      
    except applicants.DoesNotExist:
        obj=None
        return render(request,'success.html',{'application_not_submitted':'application_not_submitted'})


@login_required
def generate(request):
    try:
        current=request.user.pass_id
        expire_date=applicants.objects.get(pass_id=current).expire_date
        today=date.today()
        obj=applicants.objects.get(pass_id=current).approval
        if obj:
            #payment if loop
                if(current == 0):
                    print(current)
                    return render(request,'success.html',{'your_not_applied':'your_not_applied'})
                else:
                    if(today > expire_date):
                        messages.info(request, 'Your pass validity expired') 
                        return redirect(home)
                    else:
                        return render(request,'generate.html')
        else:
            return render(request,'success.html',{'application_not_approved':'application_not_approved'})
    except applicants.DoesNotExist:
        obj=None
        return render(request,'success.html',{'application_not_submitted':'application_not_submitted'})

        

@login_required
def pas(request):
    return render(request,'pass.html')

@login_required
def payment(request):
    pass_id=request.user.pass_id
    try:
        obj=applicants.objects.get(pass_id=pass_id).approval
        if obj:
            return render(request,'payment.html')
        else:
            messages.info(request, 'Application not approved') 
            return redirect('/')
    except applicants.DoesNotExist:
        obj=None
        messages.info(request, 'Application not subbmitted') 
        return redirect('/')
    

#def error_404(request,exception):
 #   return render(request, 'error_404.html')
def handler404(request, exception):
    return render(request,'error_404.html')
def handler500(request):
    return render(request,'error_404.html')

@login_required
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')
    
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = Account.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'yuvarajkharvi4111@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
    
   

@login_required
def pass_val(request):  
    if request.method =='POST':
        approval_id=request.POST['approval_id']
        date=request.POST['d_o_b']
        date1=parse_date(date)
        
        date2=applicants.objects.get(pass_id=approval_id).date_of_birth
        
        if date2==date1:
            data=applicants.objects.get(pass_id=approval_id)
            return render(request,'pass.html',{'data':data})
        else:
            messages.info(request, 'Wrong Date of birth')  
            return redirect('generate')

@login_required             
def renewal_auth(request):  
    if request.method =='POST':
        pass_id=request.POST['pass_id']
        date1=request.POST['d_o_b']
        date3=applicants.objects.get(pass_id=pass_id).date_of_birth
        date2=parse_date(date1)
        if (date3 == date2):
                data=applicants.objects.get(pass_id=pass_id)
                return render(request,'renewal_fill.html',{'data':data})
        else:
            messages.info(request, 'Wrong Date of birth')  
            return redirect('renewal')
       
@requires_csrf_token
def contact_form(request):
     if request.method =='POST':
         username=request.POST['username']
         email=request.POST['email']
         phone=request.POST['phone']
         message=request.POST['messages']
         data = contact_list(username=username, email=email, phone=phone, messages=message)
         data.save()
         return render(request,'contact.html',{'username':username})


@login_required
@requires_csrf_token
def apply_form(request):
    if request.method =='POST':
        admission_no=request.POST['admission_no']
        mobilenumber=request.POST['mobilenumber']
        email_id=request.POST['email_id']
        d_o_b=request.POST['d_o_b']
        student_name=request.POST['student_name']
        gender=request.POST['gender']
        fathername=request.POST['fathername']
        mothername=request.POST['mothername']
        caste=request.POST['caste']
        rd_number=request.POST['rd_number']
        institutiontype=request.POST['institutiontype']
        institutionname=request.POST['institutionname']
        institution_addr_line1=request.POST['institution_addr_line1']
        institution_addr_line2=request.POST['institution_addr_line2']
        institution_city=request.POST['institution_city']
        institution_state=request.POST['institution_state']
        institution_postal=request.POST['institution_postal']
        student_addr_line1=request.POST['student_addr_line1']
        student_addr_line2=request.POST['student_addr_line2']
        student_city=request.POST['student_city']
        student_state=request.POST['student_state']
        student_postal=request.POST['student_postal']
        course=request.POST['course']
        year=request.POST['year']
        semester=request.POST['semester']
        #mobilenumber=request.POST['mobilenumber']
        #email_id=request.POST['email_id']
        adharnumber=request.POST['adharnumber']
        fee_amount=request.POST['fee_amount']
        fromstop=request.POST['fromstop']
        tostop=request.POST['tostop']
        via1=request.POST['via1']
        #via2=request.POST['via2']
        passportsize=request.FILES['passportsize']
        collegefees=request.FILES['collegefees']
        adharcard=request.FILES['adharcard']
        studycertificate=request.FILES['studycertificate']
        previousYear=request.FILES['previousYear']
        agree=request.POST['agree']  
        #time will update after payment
        expiredate=timezone.now().date() + timedelta(days=365)
        pass_id=''.join(random.choice(string.digits) for x in range(6))
        if applicants.objects.filter(pass_id=pass_id).exists():
            pass_id=''.join(random.choice(string.digits) for x in range(6))    
        application=applicants(admission_no=admission_no,phone_number=mobilenumber,email=email_id,date_of_birth=d_o_b,student_name=student_name,gender=gender,
                                father_name=fathername,mother_name=mothername,caste=caste,rd_number=rd_number,institute_type=institutiontype,institute_name=institutionname,
                                institute_address=institution_addr_line1,inst_street_address1=institution_addr_line2,inst_city=institution_city,inst_state=institution_state,
                                inst_postal_code=institution_postal,student_address=student_addr_line1,stud_street_address1=student_addr_line2,stud_city=student_city,stud_state=student_state,
                                stud_postal_code=student_postal,course=course,year=year,semester=semester,adhar_number=adharnumber,college_fee_amt=fee_amount,from_stop=fromstop,to_stop=tostop,
                                via_1=via1,terms_cond=agree,passport_size_image=passportsize,college_fees_image=collegefees,adhar_image=adharcard,study_certificate_image=studycertificate,
                                previous_marks_image=previousYear,pass_id=pass_id,expire_date=expiredate)
        obj=Account.objects.get(email=email_id)
        obj.pass_id=pass_id
        obj.save(update_fields=['pass_id'])
        application.save() 
        messages.info(request, 'application submitted') 
        return redirect('home')

@login_required
@requires_csrf_token
def renewal_fun(request):
    if request.method =='POST':
        email=request.POST['email']
        semester=request.POST['semester']
        year=request.POST['year']
        fee_amount=request.POST['fee_amount']
        from_stop=request.POST['from_stop']
        to_stop=request.POST['to_stop']
        previous = request.FILES['previousYear']
        study_cert=request.FILES['reciept']
        reciept=request.FILES['study']
        obj=applicants.objects.get(email=email)
        #applicants.objects.filter(email=email).update(study_certificate_image=study_cert)
        obj.study_certificate_image=study_cert
        obj.previous_marks_image=previous
        obj.college_fees_image=reciept
        obj.save(update_fields=['study_certificate_image'])
        obj.save(update_fields=['previous_marks_image'])
        obj.save(update_fields=['college_fees_image'])
        obj.semester=semester
        obj.college_fee_amt=fee_amount
        obj.year=year
        obj.from_stop=from_stop
        obj.to_stop=to_stop
        obj.approval=False
        obj.save()
        
        messages.info(request, 'renewal') 
        return redirect('home')

