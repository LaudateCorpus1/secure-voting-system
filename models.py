from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    User,
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
User=settings.AUTH_USER_MODEL
choi=(
    ('1', 'Admin'),
    ('2', 'Hossam Tag'),
    ('3', 'Hassn Safty'),
    ('4', 'Hossam Mansour'),
    ('5', 'Bahaa Asem'),
    ('6', 'abedo Qasim'),
    ('7', 'Ahmed Anas'),
)

ch=(
    ('1', 'Beckenbauer'),
    ('2', 'G.Best'),
    ('3', 'Zidane'),
    ('4', 'Maradona'),
    ('5', 'Di Stefano'),
    ('6', 'Pele'),
    ('7', 'Platini'),
    ('8', 'Messi'),
    ('9', 'Cruyff'),
    ('10', 'Ronaldo'),
)



class MyUserManager(BaseUserManager):
    def create_user(self,id,phone,username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            id=id,
            phone=phone,
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            25,
            00000000000,
            username,
            email,
            password=password,

        )
        user.is_admin = True
        user.is_staff=True
        user.confirm_user=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    id             =models.CharField(max_length=5,choices=choi,default='Hossam Tag',primary_key=True)
    full_name      =models.CharField(max_length=120,null=True,blank=True)
    username       =models.CharField(max_length=30,unique=True,null=False,blank=False)
    email          =models.CharField(max_length=254,unique=True)
    password       =models.CharField(max_length=300,help_text="the password must be at least 16 chars , hint : for more powerful and memorable password you can make it sentence ")
    phone          =models.CharField(max_length=11,null=True,blank=True)
    is_vote        =models.BooleanField(default=False)
    confirm_user   =models.BooleanField(default=False)
    confirm_email  =models.BooleanField(default=False)
    confirm_code   =models.CharField(max_length=16,null=True,blank=True)
    share1          =models.ImageField(upload_to="home/hossam/Desktop/p/static_env/media_root/",null=True,blank=True)
    share2          =models.ImageField(upload_to="home/hossam/Desktop/p/static_env/media_root/",null=True,blank=True)
    owner           =models.ImageField(upload_to="home/hossam/Desktop/p/static_env/media_root/",null=True,blank=True)
    string_share   =models.CharField(max_length=40,null=True,blank=True)


    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    #
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
#
# class voters(models.Model):
#     id             =models.CharField(max_length=5,choices=choi,default='DR Mohamed Loey',primary_key=True)
#     full_name      =models.CharField(max_length=120,null=True,blank=False)
#     username       =models.CharField(max_length=30,unique=True,null=False,blank=False)
#     email          =models.CharField(max_length=254,unique=True)
#     password       =models.CharField(max_length=300,help_text="the password must be at least 16 chars , hint : for more powerful and memorable password you can make it sentence ")
#     phone          =models.CharField(max_length=11,null=True,blank=True)
#     is_vote        =models.BooleanField(default=False)
#     confirm_user   =models.BooleanField(default=False)
#     confirm_email  =models.BooleanField(default=False)
#     confirm_code   =models.CharField(max_length=1choices=choi,default='Hossam Tag'6,null=True,blank=True)
#
#
#     def __str__(self):
#         return str(voters.full_name)
class phone_user(models.Model):
    id             =models.CharField(max_length=5,choices=choi,default='DR Mohamed Loey',primary_key=True)
    phone          =models.CharField(max_length=11,null=True,blank=True)

class player_m(models.Model):

    player=models.CharField(max_length=5,choices=ch)
    name=models.CharField(max_length=120)
    no_votes=models.IntegerField(default=0)