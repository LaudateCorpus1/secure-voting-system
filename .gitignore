from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
import os
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import cv2
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm,loginform , confirm_user_form,vote_form,FPassword_form,Send_fp,vc_form,vc_form2
from .models import MyUser,player_m
from passlib.hash import pbkdf2_sha256
from random import choice
from string import  ascii_letters , digits
import random
from io import StringIO
import boto3
from django.core.mail import send_mail, EmailMessage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
import base64
# Create your views here.

User=get_user_model()

def home(request):
    form=loginform(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user_obj=User.objects.get(username__iexact=username)
        if not user_obj.confirm_user:
            return HttpResponseRedirect("/confirm")
        else:
            login(request,user_obj)
            return HttpResponseRedirect("/visual")
    return render(request,"home.html",{"form":form})




def signup(request):
    qs=MyUser.objects.filter(id=request.POST.get('id',None))
    if (qs.count()>0 ):
        if qs[0].confirm_user==0 :
            qs.delete()
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        v = MyUser.objects.filter(id=request.POST.get('id', None))
        o = ''.join(choice(ascii_letters) for i in range(16))
        a = ''.join(choice(ascii_letters) for i in range(8))
        b = ''.join(choice(ascii_letters) for i in range(8))
        c = ''.join(choice(ascii_letters) for i in range(8))
        d = ''.join(choice(ascii_letters) for i in range(8))
        e=a+' '+b+' '+c+' '+d
        img_bw = np.ones([350, 350], dtype=np.uint8) * 255
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_bw,a,(20,75),font,2,(0,0,0),5,cv2.LINE_AA)
        cv2.putText(img_bw, b, (20, 150), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
        cv2.putText(img_bw, c, (20, 225), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
        cv2.putText(img_bw, d, (20, 300), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
        image = Image.fromarray(img_bw)
        image = image.convert('1')

        outfile1 = Image.new("1", [dimension * 2 for dimension in image.size])

        outfile2 = Image.new("1", [dimension * 2 for dimension in image.size])

        for x in range(0, image.size[0], 2):
            for y in range(0, image.size[1], 2):
                sourcepixel = image.getpixel((x, y))
                assert sourcepixel in (0, 255)
                coinflip = random.random()
                if sourcepixel == 0:
                    if coinflip < .5:
                        outfile1.putpixel((x * 2, y * 2), 255)
                        outfile1.putpixel((x * 2 + 1, y * 2), 0)
                        outfile1.putpixel((x * 2, y * 2 + 1), 0)
                        outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                        outfile2.putpixel((x * 2, y * 2), 0)
                        outfile2.putpixel((x * 2 + 1, y * 2), 255)
                        outfile2.putpixel((x * 2, y * 2 + 1), 255)
                        outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    else:
                        outfile1.putpixel((x * 2, y * 2), 0)
                        outfile1.putpixel((x * 2 + 1, y * 2), 255)
                        outfile1.putpixel((x * 2, y * 2 + 1), 255)
                        outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                        outfile2.putpixel((x * 2, y * 2), 255)
                        outfile2.putpixel((x * 2 + 1, y * 2), 0)
                        outfile2.putpixel((x * 2, y * 2 + 1), 0)
                        outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                elif sourcepixel == 255:
                    if coinflip < .5:
                        outfile1.putpixel((x * 2, y * 2), 255)
                        outfile1.putpixel((x * 2 + 1, y * 2), 0)
                        outfile1.putpixel((x * 2, y * 2 + 1), 0)
                        outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                        outfile2.putpixel((x * 2, y * 2), 255)
                        outfile2.putpixel((x * 2 + 1, y * 2), 0)
                        outfile2.putpixel((x * 2, y * 2 + 1), 0)
                        outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    else:
                        outfile1.putpixel((x * 2, y * 2), 0)
                        outfile1.putpixel((x * 2 + 1, y * 2), 255)
                        outfile1.putpixel((x * 2, y * 2 + 1), 255)
                        outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                        outfile2.putpixel((x * 2, y * 2), 0)
                        outfile2.putpixel((x * 2 + 1, y * 2), 255)
                        outfile2.putpixel((x * 2, y * 2 + 1), 255)
                        outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)

        gh = ''.join(choice(ascii_letters) for i in range(16))+'.png'
        mm='/home/hossam/Desktop/p/static_env/media_root/'+gh
        ik = ''.join(choice(ascii_letters) for i in range(16))+'.png'
        ff='/home/hossam/Desktop/p/static_env/media_root/'+ik

        v.update(confirm_code=o)
        outfile1.save(mm)
        outfile2.save(ff)
        rr = ''.join(choice(ascii_letters) for i in range(16))+'.png'
        tt = ''.join(choice(ascii_letters) for i in range(16))+'.png'

        v[0].share1.save(rr,File(open(mm,'rb')))
        v[0].share2.save(tt,File(open(ff,'rb')))
        os.remove(mm)
        os.remove(ff)
        v.update(string_share=e)
        m = 'your verification code is : '+o
        k = MyUser.objects.filter(id=request.POST.get('id', None))
        try:
            mail = EmailMessage('Voting shrar 1', 'please upload this image to the voting site ', 'votesystem555@gmail.com', [k[0].email])
            mail.attach_file( k[0].share1.path)
            mail.send()
        except:
            print("network error")
        print(k)
        pho='02'+k[0].phone
        print(pho)
        client=boto3.client('sns','us-east-1')
        client.publish(PhoneNumber=pho,Message=m)
        return HttpResponseRedirect("/confirm")

    return render(request,"signup.html",{"form":form})



@login_required(login_url='/')
def vote(request):
    form=vote_form(request.POST or None)
    if form.is_valid():
        c_user = request.user
        qs = User.objects.filter(username=c_user.username)
        if c_user.confirm_email:

            player=form.cleaned_data.get("player")
            q=player_m.objects.filter(id=request.POST.get('player', None))
            x=q[0].no_votes+1
            q.update(no_votes=x)
            qs.update(is_vote=True)
            logout(request)
            return HttpResponseRedirect("/")


    return render(request,"vote.html",{"form":form})





def f_password(request):
    form=FPassword_form(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("new_username")
        password = form.cleaned_data.get("new_password")
        phone_number = form.cleaned_data.get("phone_number")
        qs = MyUser.objects.filter(username=request.POST.get('username', None))
        user_obj = User.objects.get(username=request.POST.get('username', None))
        print(user_obj)
        user_obj.set_password(password)
        user_obj.save()
        o = ''.join(choice(ascii_letters) for i in range(16))
        qs.update(confirm_code=o)
        return HttpResponseRedirect("/")

    return render(request,"f_password.html",{"form":form,})




def f_password2(request):
    form2=Send_fp(request.POST or None)
    if form2.is_valid():
        user_obj = User.objects.get(email=request.POST.get('email', None))
        co='this code is for reseting password : '+user_obj.confirm_code
        print(co)
        try:
            mail = EmailMessage('Voting shrar 1', co , 'votesystem555@gmail.com', [user_obj.email])
            mail.send()
        except:
            print("network error")
        return HttpResponseRedirect("/forgetpassword")
    return render(request,"f_password0.html",{"form2":form2})




def conf(request):
    form = confirm_user_form(request.POST or None)
    if form.is_valid():
        qs = MyUser.objects.filter(username=request.POST.get('username', None))
        qs.update(confirm_user=True)
        o = ''.join(choice(ascii_letters) for i in range(16))
        qs.update(confirm_code=o)
        return HttpResponseRedirect("/")

    return render(request,"fr.html",{"form":form})



@login_required(login_url='/')
def vc(request):
    form=vc_form(request.POST or None , request.FILES or None)
    if form.is_valid():
        pic=request.FILES['share1']
        c_user = request.user
        gh = ''.join(choice(ascii_letters) for i in range(16)) + '.png'
        infile1=Image.open(pic)
        infile2 =Image.open(c_user.share2)
        outfile = Image.new('1', infile1.size)

        for x in range(infile1.size[0]):
            for y in range(infile1.size[1]):
                outfile.putpixel((x, y), max(infile1.getpixel((x, y)), infile2.getpixel((x, y))))
        ik = ''.join(choice(ascii_letters) for i in range(16))+'.png'
        ff='/home/hossam/Desktop/p/static_env/media_root/'+ik
        outfile.save(ff)
        tt = ''.join(choice(ascii_letters) for i in range(16))+'.png'

        c_user.owner.save(tt,File(open(ff,'rb')))
        os.remove(ff)



        return HttpResponseRedirect("/visual2/")

    return render(request,"vc.html",{"form":form})


def vc2(request):
    user = request.user

    form=vc_form2(request.POST or None, request.FILES or None)
    if form.is_valid():
        captcha = form.cleaned_data.get("captcha")
        c_user = request.user
        qs = MyUser.objects.filter(username=c_user.username)
        if c_user.string_share == captcha :
            qs.update(confirm_email=True)
            return HttpResponseRedirect("/vote/")
    return render(request, "vc2.html", {"form": form, "user": user})
