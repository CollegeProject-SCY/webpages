from decimal import Context
from django import template
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail.message import utf8_charset
from django.http import request, response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.utils import timezone, translation
import random ,string
from django.conf import settings


# Create your views here.

from django.views.decorators.csrf import requires_csrf_token
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import http_date, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from .models import Account, contact_list,applicants,Route,pass_rate,depos
from django.utils.encoding import force_bytes

from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.dateparse import parse_date
from django.contrib.admin.models import LogEntry
from datetime import timedelta,date
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView








# Create your views here.
LogEntry.objects.all().delete()

def loged_in(request):
    return render(request,'index.html')

def home(request):
    depo=depos.objects.all()
    return render(request,'home.html',{'depo_list':depo})
    
    
@requires_csrf_token
def register(request):
    if request.method =='POST':
         username=request.POST['username']
         email=request.POST['email']
         phone=request.POST['phone']
         password1=request.POST['password']
         encpass=encrypt(password1)
         print(encpass)
         #pass_id=uuid.uuid4()
         
         if(Account.objects.filter(username=username).exists()):
            messages.info(request, 'username exist :(') 
            return redirect('loged_in') 
              
         elif(Account.objects.filter(email=email).exists()):
            messages.info(request, 'email exist :(') 
            return redirect('loged_in') 
    try:
        otp=''.join(random.choice(string.digits) for x in range(4))
        mail='Dear, '+username+' Please verify your Email By entering Below otp '+otp+ '.'
        send_mail('OTP', mail ,'roadwayexpressscy@gmail.com' , [email], fail_silently=False)
    except socket.gaierror:
    #except socket.error:
    #except socket.timeout:
        return render(request,'internet_error.html')
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
import socket
def resend(request):
    username=request.session['username']
    email=request.session['email']
    otp=''.join(random.choice(string.digits) for x in range(4))
    try:
        mail='Dear, '+username+' Please verify your Email By entering Below otp '+otp+ '.'
        send_mail('Email Verification', mail ,'roadwayexpressscy@gmail.com' , [email], fail_silently=False)
        request.session['otp']=otp
    except socket.gaierror:
        print("network lost")
        return render(request,'internet_error.html')
    return render(request,'otp.html',{'email':email})


def verification(request,item_id=None):
    if request.method =='POST':
        first=request.POST['first']
        second=request.POST['second']
        third=request.POST['third']
        fourth=request.POST['fourth']
        user_otp=first+second+third+fourth
        try:
            username=request.session['username']
            phone=request.session['phone']
            #re_otp=request.session['re_otp']
            encpass=request.session['encpass']
            email=request.session['email']
            otp=request.session['otp']
            
            if (user_otp==otp):
                user_obj =Account.objects.create(username=username, phone=phone, email=email, password=encpass)
                user_obj.set_password(encpass)
                user_obj.save()
                messages.info(request, 'Account Created Successfully :)')  
                print(' user created '+username) 
                return redirect('loged_in')
            else:
                return render(request,'otp.html',{'wrong_otp':'wrong_otp'})
        except KeyError:
            messages.info(request, 'OTP is Expired')
            return redirect(loged_in)

def log_in(request):  
    if request.method =='POST':
          username=request.POST['username']
          password=request.POST['password']  
          encpass=encrypt(password)
          #email=Account.objects.get(email=username).email
          if(Account.objects.filter(username=username).exists()):
                user = Account.objects.get(username=username)
                
                if user.check_password(encpass):
                    login(request, user)
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    print('User loged '+username)
                    
                    return redirect('home')
                else:
                   
                    return render(request,'index.html',{'pass':password})
          elif(Account.objects.filter(email=username).exists()):
                user = Account.objects.get(email=username)
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

def encrypt(pssword):
        x = "1".join(pssword)
        x1 = x.upper()
        return(x1)

class customSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        password=encrypt(self.cleaned_data["new_password1"])
        print(password)
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class customPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=customSetPasswordForm
         
def contact_us(request):
    return render(request,'contact.html')

def about_us(request):
    return render(request,'about.html')

@login_required
def apply(request):
    current=request.user.pass_id
    if(current == '0'):
        return render(request,'apply.html')
    else:
        print(current)
        return render(request,'success.html',{'your_already_applied':current})

def view(request):
    pass_amts=pass_rate.objects.all()
    dests=Route.objects.all()
    return render(request,'view.html',{'dests':dests, 'pass_amts':pass_amts})

@login_required
def renewal(request):
    try:
        current=request.user.pass_id
        username=request.user.username
        try:
            expire_date=Transaction.objects.get(username=username).expire_date
            status=Transaction.objects.get(username=username).status
        except Transaction.DoesNotExist:
            status=None
            expire_date=None
            return render(request,'success.html',{'application_not_approved':'application_not_approved'})
        obj=applicants.objects.get(pass_id=current).approval
        if status=='Renew':
            return render(request,'success.html',{'under_renew':'under_renew'})
        else:
            if obj:    
                
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
        return render(request,'success.html',{'application_not_submitted_renw':'application_not_submitted_renw'})


@login_required
def generate(request):
    try:
        current=request.user.pass_id
        username=request.user.username
        
        today=date.today()
        try:
            status=Transaction.objects.get(username=username).status
            expire_date=Transaction.objects.get(username=username).expire_date
        except Transaction.DoesNotExist:
            status=None
            expire_date=None
            return render(request,'success.html',{'application_not_approved':'application_not_approved'})
        obj=applicants.objects.get(pass_id=current).approval
        if obj:
            #payment if loop
                print(status)
                if(current == 0):
                    print(current)
                    return render(request,'success.html',{'your_not_applied':'your_not_applied'})
                else:
                    if(today > expire_date):
                        messages.info(request, 'Your pass validity expired') 
                        return redirect(home)
                    else:
                        if status=='Success':
                            return render(request,'generate.html')
                        else:
                            #messages.info(request, 'Payment Not Paid') 
                            return render(request,'success.html',{'Payment_pending':'Payment_pending'})
        else:
            return render(request,'success.html',{'application_not_approved':'application_not_approved'})
    except applicants.DoesNotExist:
        obj=None
        return render(request,'success.html',{'application_not_submitted':'application_not_submitted'})

        

@login_required
def pas(request):
    return render(request,'pass.html')



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
						send_mail(subject, email, 'roadwayexpressscy@gmail.com' , [user.email], fail_silently=False)
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
            username=request.user.username
            expire=Transaction.objects.get(username=username).expire_date
            return render(request,'pass.html',{'data':data,'expire':expire})
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
        #mobilenumber=request.POST['mobilenumber']
        #email_id=request.POST['email_id']
        adharnumber=request.POST['adharnumber']
        fee_amount=request.POST['fee_amount']
        fromstop=request.POST['fromstop']
        tostop=request.POST['tostop']
        #via2=request.POST['via2']
        passportsize=request.FILES['passportsize']
        collegefees=request.FILES['collegefees']
        adharcard=request.FILES['adharcard']
        studycertificate=request.FILES['studycertificate']
        previousYear=request.FILES['previousYear']
        agree=request.POST['agree']  
        #time will update after payment
        #expiredate=timezone.now().date() + timedelta(days=365)
        pass_id='EXPRESS'+''.join(random.choice(string.digits) for x in range(6))
        if applicants.objects.filter(pass_id=pass_id).exists():
            pass_id='EXPRESS'+''.join(random.choice(string.digits) for x in range(6))    
        application=applicants(admission_no=admission_no,phone_number=mobilenumber,email=email_id,date_of_birth=d_o_b,student_name=student_name,gender=gender,
                                father_name=fathername,mother_name=mothername,caste=caste,rd_number=rd_number,institute_type=institutiontype,institute_name=institutionname,
                                institute_address=institution_addr_line1,inst_street_address1=institution_addr_line2,inst_city=institution_city,inst_state=institution_state,
                                inst_postal_code=institution_postal,student_address=student_addr_line1,stud_street_address1=student_addr_line2,stud_city=student_city,stud_state=student_state,
                                stud_postal_code=student_postal,course=course,year=year,adhar_number=adharnumber,college_fee_amt=fee_amount,from_stop=fromstop,to_stop=tostop,
                                terms_cond=agree,passport_size_image=passportsize,college_fees_image=collegefees,adhar_image=adharcard,study_certificate_image=studycertificate,
                                previous_marks_image=previousYear,pass_id=pass_id)
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
        username=request.user.username
        pay_obj=Transaction.objects.get(username=username)
        email=request.POST['email']
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
        obj.college_fee_amt=fee_amount
        obj.year=year
        obj.from_stop=from_stop
        obj.to_stop=to_stop
        obj.approval=False
        obj.mail_send=False
        obj.bus_amount=0
        pay_obj.status='Renew'
        path=MEDIA_ROOT + "/receipt/" + obj.pass_id+".pdf"
        os.remove(path)
        print(path)
        obj.save()
        pay_obj.save()
        
        messages.info(request, 'renewal') 
        return redirect('home')

from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

def initiate_payment(request):
    username = request.user.username
    pass_id=request.user.pass_id
    try:
        email=applicants.objects.get(pass_id=pass_id).email
    except applicants.DoesNotExist:
        email=None
    order_id='ROADWAY'+''.join(random.choice(string.digits) for x in range(5))
    #if Transaction.objects.filter(username=username).exists():
        #order_id='ROADWAY'+''.join(random.choice(string.digits) for x in range(5))
    if request.method == "GET":
         
        try:
            pass_id=request.user.pass_id
            username=request.user.username
            value=applicants.objects.get(pass_id=pass_id)
            try:
                status=Transaction.objects.get(username=username).status
            except Transaction.DoesNotExist:
                status=None
            obj=applicants.objects.get(pass_id=pass_id).approval
            if obj:
                if pass_id==0:
                    return render(request,'success.html',{'your_not_applied_pay':'your_not_applied_pay'}) 
                else:
                    if status=='Success':
                        download_pass(request)
                        #messages.info(request, 'Your Already Paid')
                        return render(request, 'callback.html') 
                    else:
                        return render(request, 'pay.html',{'usr':value,'order_id':order_id})
            else:
                return render(request,'success.html',{'application_not_approved_pay':'application_not_approved_pay'}) 
        except applicants.DoesNotExist:
            value=None
        return render(request,'success.html',{'application_not_submitted':'application_not_submitted'})  
    try:
        global usr
        usr=request.user
        
        ###
        #order_id=applicants.objects.get(pass_id=pass_id).payment_id
       
        amount = int(request.POST['amount'])

        if(Account.objects.filter(username=username).exists()):
                user = Account.objects.get(username=username)
                if user is None:
                    raise ValueError
        #user = authenticate(request, username=username, password=password)
        #if user is None:
         #   raise ValueError
       # auth_login(request=request, user=user)
    
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})
    #transaction = Transaction.objects.create(amount=amount)
    #transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(order_id)),
        ('CUST_ID', str(email)),
        ('TXN_AMOUNT', str(amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )
    
    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    #transaction.checksum = checksum
    #transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        try:        
            username=usr.username
            pass_id=usr.pass_id
            mail=usr.email
            expire_date=timezone.now().date() + timedelta(days=365)
            received_data = dict(request.POST)
            paytm_params = {}
            paytm_checksum = received_data['CHECKSUMHASH'][0]
            order_id=received_data['ORDERID'][0]
            status=received_data['STATUS'][0]
            amount=received_data['TXNAMOUNT'][0]
            print(amount)
            if amount=='1400.00':
                category='OBC/General'
                amt='1200.00'
                print(category,amount)
            else:
                category='SC/ST'
                print(category,amount)
                amt='00.00'
            
            data=applicants.objects.get(pass_id=pass_id)
            
            Context={
                'data':data,
                'ORDERID':received_data['ORDERID'][0],
                'date':received_data['TXNDATE'][0],
                'category':category,
                'amount':amount,
                'amt':amt,
                'total':'200.00',
                'usr':usr,
            }
            print(Context)
            #print(received_data)
            
            #mail='Your sotp is  to visit  Apply Procedures'
            #sendimg mail
            
            for key, value in received_data.items():
                #print(key,value)
                if key == 'CHECKSUMHASH':
                    paytm_checksum = value[0]
                else:
                    paytm_params[key] = str(value[0])
            # Verify checksum
            #print(usr)
            #login(request,usr)
            #trans=Transaction.objects.create(amount=100)
            #trans.save()
            is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
            if is_valid_checksum:
                received_data['message'] = "Checksum Matched"
            else:
                received_data['message'] = "Checksum Mismatched"
            if status=='TXN_SUCCESS':
                valid_status='Success'
                #app_obj=Transaction.objects.get(username=username)
                
                receipt(request,Context,pass_id)
                
                try:
                    send_mail('Payment Successful', 'Thank you for making payment.Your Payment for bus pass is successfully Done.Please Generate Your Pass' ,'roadwayexpressscy@gmail.com' , [mail], fail_silently=False)
                except socket.gaierror:
                    return render(request,'internet_error.html')
                if Transaction.objects.filter(username=username).exists():
                    obj=Transaction.objects.get(username=username)
                    obj.status='Success'
                    obj.expire_date=expire_date
                    obj.order_id=order_id
                    Context['expire_date']=expire_date
                    bus_pass(request,Context,pass_id)
                    obj.save()
                    return render(request, 'callback.html', context=received_data)
                else:
                    trans=Transaction(username=username,order_id=order_id,status=valid_status,amount=amount,expire_date=expire_date)
                    Context['expire_date']=expire_date
                    bus_pass(request,Context,pass_id)
                    trans.save()
                    
                    print(received_data)
                    return render(request, 'callback.html', context=received_data)
                
            if status=='TXN_FAILURE':
                valid_status='Failure'

                Context={
                'message':received_data['RESPMSG'][0],
                'valid_status':'valid_status',
                }
                if Transaction.objects.filter(username=username).exists():
                    obj=Transaction.objects.get(username=username)
                    obj.status='Failure'
                    obj.order_id=order_id
                    obj.save()
                    return render(request, 'callback.html',context=Context)

                else:
                    trans=Transaction(username=username,order_id=order_id,status=valid_status,amount=amount)
                    trans.save()
                    return render(request, 'callback.html',context=Context)
                #print(verified)
                
            return render(request, 'callback.html', context=received_data)
        except NameError:
            return redirect('home')

from weasyprint import HTML,CSS
from college.settings import MEDIA_ROOT
import tempfile
import os

def receipt(request,context,pass_id):
    #username=request.user.username
    #pass_id=request.user.pass_id
    #obj=applicants.objects.get(pass_id=pass_id)
    receipt_obj=applicants.objects.get(pass_id=pass_id)
    html_string = render_to_string('receipt.html',context,request=request)
    html = HTML(string=html_string, base_url='request.build_absolute_uri()')
    result = html.write_pdf(presentational_hints=True)
    # Creating http response
    """response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=examform.pdf'
    response['Content-Transfer-Encoding'] = 'UTF-8'"""
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        receipt_obj.receipt_pdf.save(receipt_obj.pass_id+".pdf",output)
        #expaid.form_image.save(expaid.register_no+".pdf",output)

from django.http import FileResponse
def download_pass(request):
    try:
        print("download")
        try:
            pass_id=usr.pass_id
        except NameError:
            pass_id=request.user.pass_id
        '''context['bton']=False
        context['pdf']=True
        print(context['bton'])'''
        download_obj=applicants.objects.get(pass_id=pass_id)
        file_name=download_obj.pass_id+".pdf"
        response = FileResponse(open(MEDIA_ROOT + "/receipt/" + file_name, 'rb')) 
        return response
    except OSError as e:
        messages.info(request, 'Payment Not Completed!') 
        return redirect(home)
    #session error usr
    '''
     delete from hello_transaction where id>10;
    [01/Sep/2021 20:51:56] "POST /pay/ HTTP/1.1" 200 1288
{'received': {'CURRENCY': ['INR'], 'GATEWAYNAME': ['WALLET'], 'RESPMSG': ['Txn Success'], 'BANKNAME': ['WALLET'], 'PAYMENTMODE': ['PPI'], 'MID': ['Ztanbx42738781439498'], 'RESPCODE': ['01'], 'TXNID': ['20210901111212800110168438402932891'], 'TXNAMOUNT': ['340.00'], 'ORDERID': ['ROADWAY38971'], 'STATUS': ['TXN_SUCCESS'], 'BANKTXNID': ['65219189'], 'TXNDATE': ['2021-09-01 20:51:57.0'], 'CHECKSUMHASH': ['YItBYpWdTcCFwmSnUoDrbDHE7JuHIFkAPDnB92uFYis0/P1RuMOqc0/lpsL4kHO3eNmTzS1nVrv5WYllfXeE7Xr9TqzN+VKxm80QV0LtTFA=']}, 'ORDERID': 'ROADWAY38971', 'category': 'SC/ST', 'amount': '00.00', 'total': '120', 'usr': <SimpleLazyObject: <Account: yuvarajkharvi4111@gmail.com pbkdf2_sha256$260000$GROWglQykoCavjw1XDzKvM$tDOGWTxuPHv0Flu9NOKdHBETTpC6oqoEyr1RHUK5fmY=>>}
/home/yuvaraj/project/webpages/college/hello/views.py changed, reloading.
Watching for file changes with StatReloader
    '''
def bus_pass(request,context,pass_id):
    
    receipt_obj=applicants.objects.get(pass_id=pass_id)
    html_string = render_to_string('pass_download.html',context,request=request)
    html = HTML(string=html_string, base_url='request.build_absolute_uri()')
    result = html.write_pdf(presentational_hints=True)
    # Creating http response
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        receipt_obj.user_pass.save(receipt_obj.pass_id+".pdf",output)
        #expaid.form_image.save(expaid.register_no+".pdf",output)

from django.http import FileResponse
def download(request):
    try:
        print("download")
        pass_id=request.user.pass_id
        download_obj=applicants.objects.get(pass_id=pass_id)
        file_name=download_obj.pass_id+".pdf"
        response = FileResponse(open(MEDIA_ROOT + "/passes/" + file_name, 'rb')) 
        return response
    except OSError as e:
        messages.info(request, 'Pass Not Distributed!') 
        return redirect(home)   