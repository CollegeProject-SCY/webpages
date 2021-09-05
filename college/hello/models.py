from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not phone:
            raise ValueError("Users must have a contact no")

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,phone,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    phone=models.CharField(max_length=10)
    pass_id=models.CharField(max_length=20,default=0, editable=False)
   
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone']

    objects=MyAccountManager()

    def __str__(self):
        return self.email+" "+self.password

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table='login_account'
        verbose_name='Account List'



class applicants(models.Model):
    admission_no=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=13)
    date_of_birth=models.DateField(null=True, blank=True)
    student_name=models.CharField(max_length=30)
    gender=models.CharField(max_length=10)
    father_name=models.CharField(max_length=30)
    mother_name=models.CharField(max_length=30)
    caste=models.CharField(max_length=30)
    rd_number=models.CharField(max_length=10)
    institute_type=models.CharField(max_length=20)
    institute_name=models.CharField(max_length=100)
    institute_address=models.CharField(max_length=255)
    inst_street_address1=models.CharField(max_length=255)
    inst_city=models.CharField(max_length=20)
    inst_state=models.CharField(max_length=20)
    inst_postal_code=models.CharField(max_length=7)
    student_address=models.CharField(max_length=255)
    stud_street_address1=models.CharField(max_length=255)
    stud_city=models.CharField(max_length=20)
    stud_state=models.CharField(max_length=20)
    stud_postal_code=models.CharField(max_length=7)
    course=models.CharField(max_length=20)
    year=models.CharField(max_length=10)
    adhar_number=models.CharField(max_length=12)
    college_fee_amt=models.CharField(max_length=10)
    from_stop=models.CharField(max_length=50)
    to_stop=models.CharField(max_length=50)
    #via_1=models.CharField(max_length=50)
    passport_size_image=models.ImageField(upload_to='photos/')
    college_fees_image=models.ImageField(upload_to='photos/')
    adhar_image=models.ImageField(upload_to='photos/')
    study_certificate_image=models.ImageField(upload_to='photos/')
    previous_marks_image=models.ImageField(upload_to='photos/')
    terms_cond=models.BooleanField(default=False)
    pass_id=models.CharField(max_length=20, unique=True, editable=False)
    approval=models.BooleanField(default=False)
    mail_send=models.BooleanField(default=False)
    #payment_id=models.CharField(max_length=100, null=True, blank=True)
    bus_amount = models.IntegerField(null=True,default=0,blank=True)
    receipt_pdf=models.FileField(upload_to='receipt/',null=True,blank=True)
    user_pass=models.FileField(upload_to='passes/',null=True,blank=True)
    class Meta:
        db_table='application_db'
        verbose_name='Application List'

class contact_list(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=60)
    phone=models.CharField(max_length=11)
    messages=models.CharField(max_length=1000)

    class Meta:
        db_table = 'contact_table'
        verbose_name = 'Contact list'

class Route(models.Model):
    From_place=models.CharField(max_length=255)
    To_place=models.CharField(max_length=255)
    Timings=models.CharField(max_length=255)
    Bus_Number=models.CharField(max_length=20)

    class Meta:
        db_table = 'route_table'
        verbose_name = 'Route list'

class pass_rate(models.Model):
    category=models.CharField(max_length=255)
    pass_price=models.IntegerField()
    processing_fee=models.IntegerField()

    class Meta:
        db_table = 'pass_rate_table'
        verbose_name = 'Pass amounts list'

class depos(models.Model):
    city=models.CharField(max_length=255)
    bus_photo=models.ImageField(upload_to='bus_photos/')
    address=models.CharField(max_length=255)

    class Meta:
        db_table = 'Bus_Depos'
        verbose_name = 'New Bus Depo'

from django.contrib.auth import get_user_model    
#User = get_user_model() 
class Transaction(models.Model):
   # made_by = models.ForeignKey(User, related_name='transactions', 
    #                            on_delete=models.CASCADE)
    #username=models.CharField(max_length=30)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=30)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    #checksum = models.CharField(max_length=1000, null=True, blank=True)
    username=models.CharField(unique=True, max_length=100, null=True, blank=True)
    status=models.CharField(max_length=1000)
    expire_date=models.DateField(null=True, blank=True)
    #def save(self, *args, **kwargs):
    #    if self.order_id is None and self.made_on and self.id:
       #     self.order_id = self.made_on.strftime('RDW%Y%m%dODR') + str(self.id)
        #return super().save(*args, **kwargs)