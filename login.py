﻿#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re
from conn import crmdb
from zz91page import *
db = crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')

def login(request):
    return render_to_response('login/login.html',locals())
def logincheck(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username and password:
        sql='select id from user where username=%s and password=%s and closeflag=0'
        result=db.fetchonedb(sql,[username,password])
        if result:
            user_id=result['id']
            request.session.set_expiry(6000*6000)
            request.session['user_id']=user_id
            request.session['username']=username
            return HttpResponseRedirect('main.html')
        else:
            errtext="用户名或密码错误"
            return render_to_response('login/login.html',locals())
    else:
        errtext="请输入用户名或密码"
        return render_to_response('login/login.html',locals())
def logout(request):
    try:
        del request.session['username']
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect("login.html")
def socketchat(request):
    return render_to_response('login/socket.html',locals())