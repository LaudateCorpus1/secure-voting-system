from django import forms
from .models import MyUser,phone_user,player_m
from passlib.hash import pbkdf2_sha256
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.forms import ReadOnlyPasswordHashField



User=get_user_model()
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField( widget=forms.TextInput(attrs={'autocomplete': 'off'}),help_text="*the password must be at least 16 chars , hint : for more powerful and memorable password you can make it sentence " )



    class Meta:
        model = User
        fields = ('id','full_name','username','phone','email','password')

    def clean(self):
        phonee = self.cleaned_data.get("phone")
        id = self.cleaned_data.get("id")
        for i in phonee:
            if not i.isdigit():
                raise forms.ValidationError("* only numbers are allowed")
        try:
            qs = phone_user.objects.filter(phone=phonee)
            if not qs[0].id == id:
                raise forms.ValidationError("* this is not the number of this user ")
        except:
            raise forms.ValidationError("* this is not the number of this user ")
        email = self.cleaned_data.get("email")
        if (not "@" in email) or (not "." in email):
            raise forms.ValidationError("  * this is not a vaild email ")
        password = self.cleaned_data.get("password")
        if len(password) < 16:
            raise forms.ValidationError("* check the password length")

    # def clean_email(self,*args,**kwargs):
    #     email=self.cleaned_data.get("email")
    #     if( not "@" in email ) or (not "." in email ) :
    #         raise forms.ValidationError ("  * this is not a vaild email ")
    #     return email
    # def clean_password(self):
    #     password=self.cleaned_data.get("password")
    #     if len(password)<16:
    #         raise forms.ValidationError ("* check the password length")
    #     return password
    # def clean_phone(self):
    #     phonee=self.cleaned_data.get("phone")
    #     id=self.cleaned_data.get("id")
    #     for i in phonee:
    #         if not i.isdigit():
    #             raise forms.ValidationError("* only numbers are allowed")
    #     try:
    #         qs = phone_user.objects.filter(phone=phonee)
    #         if not qs[0].id == id:
    #             raise forms.ValidationError("* this is not the number of this user ")
    #     except:
    #         raise forms.ValidationError("* this is not the number of this user ")
    #     return phonee


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username','phone','email', 'full_name','password', 'is_staff', 'is_active', 'is_admin','is_vote','confirm_user','confirm_email','confirm_code')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]




# class signupform (forms.ModelForm):
#     username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
#     password = forms.CharField( widget=forms.TextInput(attrs={'autocomplete': 'off'}), )
#     class Meta:
#         model=MyUser
#         fields=['id',
#                 'full_name',
#                 'username',
#                 'email',
#                 'phone',
#                 'password',
#                ]
#     def clean_email(self,*args,**kwargs):
#         email=self.cleaned_data.get("email")
#         if( not "@" in email ) or (not "." in email ) :
#             raise forms.ValidationError ("  * this is not a vaild email ")
#         return email
#     def clean_password(self):
#         password=self.cleaned_data.get("password")
#         if len(password)<16:
#             raise forms.ValidationError ("* check the password length")
#         return password
#     def clean_phone(self):
#         phonee=self.cleaned_data.get("phone")
#         id=self.cleaned_data.get("id")
#         for i in phonee:
#             if not i.isdigit():
#                 raise forms.ValidationError("* only numbers are allowed")
#         try:
#             qs = phone_user.objects.filter(phone=phonee)
#             if not qs[0].id == id:
#                 raise forms.ValidationError("* this is not the number of this user ")
#         except:
#             raise forms.ValidationError("* this is not the number of this user ")
#         return phonee




class loginform (forms.Form):
    username=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        user_obj=User.objects.filter(username=username).first()

        if not user_obj:
            raise forms.ValidationError(" CHECK YOUR USERNAME AND PASSWORD ")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError(" CHECK YOUR USERNAME AND PASSWORD ")
        if user_obj.is_admin:
            raise forms.ValidationError(" CHECK YOUR USERNAME AND PASSWORD ")
        # if not user_obj.confirm_user:
        #     raise forms.ValidationError(" PLEASE, CONFIRM YOUR ACCOUNT ")
        if user_obj.is_vote:
            raise forms.ValidationError(" THIS USER ALREADY VOTED ")

        return super (loginform,self).clean()




class confirm_user_form (forms.Form):
    username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(min_length=16, widget=forms.TextInput(attrs={'autocomplete': 'off'}) )
    code     = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    x=False
    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        code=self.cleaned_data.get("code")
        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            raise forms.ValidationError(" CHECK YOUR USERNAME AND PASSWORD ")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError(" CHECK YOUR USERNAME AND PASSWORD ")

            if not code==user_obj.confirm_code :
                raise forms.ValidationError("this is not right code")

class vote_form (forms.ModelForm):


    class Meta:
        model=player_m
        fields = ['player']
    def x(request):
        user=request.user
        return user.username
class FPassword_form (forms.Form):
    username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    new_password = forms.CharField(min_length=16, widget=forms.TextInput(attrs={'autocomplete': 'off'}) )
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    code         = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    x=False
    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        code=self.cleaned_data.get("code")
        phone_number=self.cleaned_data.get("phone_number")
        user_obj = User.objects.filter(phone=phone_number).first()

        if not user_obj:
            raise forms.ValidationError(" Invaild Data ")

        if not code == user_obj.confirm_code:
            raise forms.ValidationError(" Invaild Data ")
class Send_fp (forms.Form):
    email=forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    def clean(self):
        email=self.cleaned_data.get("email")
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError(" Invaild email ")


class vc_form (forms.Form):
    share1= forms.ImageField()

class vc_form2 (forms.Form):
    captcha=forms.CharField(max_length=120, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def clean(self):

        cap=self.cleaned_data.get("captcha")
