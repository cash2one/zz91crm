#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
import calendar as cal
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db=crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/hr_function.py")
zzs=zzhr()

#取出所有人员信息
def hr_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    star=request.GET.get("star")
    if star:
         searchlist['star']=star
    username=request.GET.get("username")
    if username:
        searchlist['username']=username
    mobile=request.GET.get("mobile")
    if mobile:
        searchlist['mobile']=mobile
    email=request.GET.get("email")
    if email:
        searchlist['email']=email
    sex=request.GET.get("sex")
    if sex:
        searchlist['sex']=sex
    jl1=request.GET.get("jl1")
    if jl1:
        searchlist['jl1']=jl1
    jl2=request.GET.get("jl2")
    if jl2:
        searchlist['jl2']=jl2
    jl3=request.GET.get("jl3")
    if jl3:
        searchlist['jl3']=jl3
    jl4=request.GET.get("jl4")
    if jl4:
        searchlist['jl4']=jl4
    jl5=request.GET.get("jl5")
    if jl5:
        searchlist['jl5']=jl5
    personid=request.GET.get("personid")
    if personid:
        searchlist['personid']=personid
    rpersonid=request.GET.get("rpersonid")
    if rpersonid:
        searchlist['rpersonid']=rpersonid
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.gethrlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('hr/hr_list.html',locals())
#添加人员
def hr_add(request):
    username=request.POST.get('username')
    sex=request.POST.get('sex')
    mobile=request.POST.get('mobile')
    email=request.POST.get('email')
    education=request.POST.get('education')
    interviewTime=request.POST.get('interviewTime')
    laiyuan=request.POST.get('laiyuan')
    star=request.POST.get('star')
    jl1=request.POST.get('jl1')
    jl2=request.POST.get('jl2')
    jl3=request.POST.get('jl3')
    jl4=request.POST.get('jl4')
    jl5=request.POST.get('jl5')
    othercontact=request.POST.get('othercontact')
    station=request.POST.get('station')
    
    if username:
        sql='insert into renshi_user(username,sex,mobile,email,education,interviewTime,laiyuan,star,jl1,jl2,jl3,jl4,jl5,othercontact,station) values(%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result=db.updatetodb(sql,[username,sex,mobile,email,education,interviewTime,laiyuan,star,jl1,jl2,jl3,jl4,jl5,othercontact,station])
        return HttpResponseRedirect('list.html')
    return render(request,'hr/hr_add.html')
#修改人员信息
def hr_mod(request):
    if request.method=="POST":
        star=request.POST.get('star')
        username=request.POST.get('username')
        sex=request.POST.get('sex')
        mobile=request.POST.get('mobile')
        station=request.POST.get('station')
        jl1=request.POST.get('jl1')
        jl2=request.POST.get('jl2')
        jl3=request.POST.get('jl3')
        jl4=request.POST.get('jl4')
        jl5=request.POST.get('jl5')
        email=request.POST.get("email")
        education=request.POST.get('education')
        interviewTime=request.POST.get('interviewTime')
        laiyuan=request.POST.get('laiyuan')
        id=request.GET.get('id')
        if username:
            sql='update renshi_user set star=%s,username=%s,sex=%s,mobile=%s,station=%s,jl1=%s,jl2=%s,jl3=%s,jl4=%s,jl5=%s,email=%s,education=%s,interviewTime=%s,laiyuan=%s where id=%s'
            result=db.updatetodb(sql,[star,username,sex,mobile,station,jl1,jl2,jl3,jl4,jl5,email,education,interviewTime,laiyuan,id])
        return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('id')
        if id:
            sql='select * from renshi_user where id=%s'
            result=db.fetchonedb(sql,[id])
            return render_to_response('hr/hr_mod.html',locals())
#删除人员信息
def hr_del(request):
     id=request.GET.get('id')
     if id:
        sql='delete from renshi_user where id=%s'
        result=db.updatetodb(sql,[id])
        return HttpResponseRedirect('list.html')
#批量删除
def hr_delall(request):
    check_box_list = request.REQUEST.getlist("check_box_list")
    for id in check_box_list:
        sql='delete from renshi_user where id=%s'
        result=db.updatetodb(sql,[id])
    return HttpResponseRedirect('list.html')
#单独界面显示个人信息
def hr_usershow(request):
    if request.method=="POST":
        uid=request.GET.get('uid')
        contactstat=request.POST.get('contactstat')
        selectjl=request.POST.get('selectjl')
        if selectjl=="1":
            code=request.POST.get('jl1')
        if selectjl=="2":
            code=request.POST.get('jl2')
        if selectjl=="3":
            code=request.POST.get('jl3')
        if selectjl=="4":
            code=request.POST.get('jl4')
        if selectjl=="5":
            code=request.POST.get('jl5')
        star=request.POST.get('star')
        nextteltime=request.POST.get('nextteltime')
        bz=request.POST.get('bz')
        user_id=request.session.get('user_id',default=None)
        if uid:
            sql='insert into renshi_history(contactstat,code,star,nextteltime,bz,uid,personid) values(%s,%s,%s,%s,%s,%s,%s)'
            result=db.updatetodb(sql,[contactstat,code,star,nextteltime,bz,uid,user_id])
        return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('uid')
        if id:
            sql='select * from renshi_user where id=%s'
            result=db.fetchonedb(sql,[id])
            education=result['education']
            sql1='select * from renshi_category where code=%s'
            result1=db.fetchonedb(sql1,[education])
            result['education']=result1['label']
            return render_to_response('hr/hr_usershow.html',locals())
#操作记录
def hr_usershow_history(request):
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    uid=request.GET.get('uid')
    if uid:
        searchlist['uid']=uid
    funpage=zz91page()
    limitNum=funpage.limitNum(4)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getrenshihistory(searchlist=searchlist,frompageCount=frompageCount,limitNum=limitNum)
    listall=userallr['list']
    listcount=userallr['count']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('hr/hr_usershow_history.html',locals())
    
#更改面试状态
def hr_station(request):
    id=request.GET.get('id')
    station=request.GET.get('station')
    jl1=request.GET.get('jl1')
    jl2=request.GET.get('jl2')
    jl3=request.GET.get('jl3')
    jl4=request.GET.get('jl4')
    jl5=request.GET.get('jl5')
    education=request.GET.get('education')
    if id:
        if station:
             sql="update renshi_user set station=%s where id=%s"
             result=db.updatetodb(sql,[station,id])
        if jl1:
             sql="update renshi_user set jl1=%s where id=%s"
             result=db.updatetodb(sql,[jl1,id])
        if jl2:
             sql="update renshi_user set jl2=%s where id=%s"
             result=db.updatetodb(sql,[jl2,id])
        if jl3:
            sql="update renshi_user set jl3=%s where id=%s"
            result=db.updatetodb(sql,[jl3,id])
        if jl4:
            sql="update renshi_user set jl4=%s where id=%s"
            result=db.updatetodb(sql,[jl4,id])
        if jl5:
            sql="update renshi_user set jl5=%s where id=%s"
            result=db.updatetodb(sql,[jl5,id])
        if education:
            sql="update renshi_user set education=%s where id=%s"
            result=db.updatetodb(sql,[education,id])
        return HttpResponseRedirect('list.html')
#人事基础数据
def hr_basic(request):
    searchlist={}
    label=request.GET.get('label')
    if label:
        searchlist['label']=label
    userallr=zzs.gethrbasiclist(searchlist=searchlist)
    listall=userallr['list']
    return render_to_response('hr/hr_basic.html',locals())
#添加人事基础数据
def hr_basic_add(request):
    code=request.GET.get('code')
    if code:
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        if label:
            sql="select count(0) as count from renshi_category where code like %s"
            code1=str(db.fetchonedb(sql,[""+code+"__"])['count']+1)
            code1=code1.zfill(2)
            code=code+code1
            sql="insert into renshi_category(code,label,ord) values(%s, %s, %s)"
            result=db.updatetodb(sql,[code,label,ord])
            return HttpResponseRedirect('basic.html')
        return render(request,'hr/hr_basic_add.html')
    else:
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        if label:
            sql="select max(left(code,2))+1 from renshi_category"
            code=db.fetchonedb(sql)['max(left(code,2))+1']
            sql="insert into renshi_category (code,label,ord) values(%s, %s, %s)"
            result=db.updatetodb(sql,[code,label,ord])
            return HttpResponseRedirect('basic.html')
        return render(request,'hr/hr_basic_add.html')
#修改人事基础数据
def hr_basic_mod(request):
    if request.method=="POST":
        label=request.POST.get('label')
        ord=request.POST.get('ord')
        id=request.GET.get('id')
        if label:
            sql='update renshi_category set label=%s,ord=%s where id=%s'
            result=db.updatetodb(sql,[label,ord,id])
        return HttpResponseRedirect('basic.html')
    else:
        id=request.GET.get('id')
        if id:
            sql='select * from renshi_category where id=%s'
            result=db.fetchonedb(sql,[id])
            return render_to_response('hr/hr_basic_mod.html',locals())
#删除人事基础数据
def hr_basic_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from renshi_category where id=%s'
        result=db.updatetodb(sql,[id])
        return HttpResponseRedirect('basic.html')
