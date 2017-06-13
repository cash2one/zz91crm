#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
import calendar as cal
from conn1 import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db=crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/news_function.py")
zzs=zznews()

#所有新闻
def news_list(request):
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
    
    funpage=zz91page()
    limitNum=funpage.limitNum(15)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getnewslist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('news/news_list.html',locals())
#添加新闻
def news_add(request):
    subject=request.POST.get('subject')
    hit=request.POST.get('hit')
    if subject:
        sql='insert into bz_article(subject,hit) values(%s, %s)'
        result=db.updatetodb(sql,[subject,hit])
        return HttpResponseRedirect('list.html')
    return render(request,'news/news_add.html')
#修改新闻
def news_mod(request):
    if request.method=="POST":
        aid=request.GET.get('aid')
        subject=request.POST.get('subject')
        hit=request.POST.get('hit')
        if subject:
            sql='update bz_article set subject=%s,hit=%s where aid=%s'
            result=db.updatetodb(sql,[subject,hit,aid])
        return HttpResponseRedirect('list.html')
    else:
        aid=request.GET.get('aid')
        if aid:
            sql='select subject,hit from bz_article where aid=%s'
            result=db.fetchonedb(sql,[aid])
            return render_to_response('news/news_mod.html',locals())
#删除新闻
def news_del(request):
     aid=request.GET.get('aid')
     if aid:
        sql='delete from bz_article where aid=%s'
        result=db.updatetodb(sql,[aid])
        return HttpResponseRedirect('list.html')
#批量删除
def hr_delall(request):
    check_box_list = request.REQUEST.getlist("check_box_list")
    for id in check_box_list:
        sql='delete from renshi_user where id=%s'
        result=db.updatetodb(sql,[id])
    return HttpResponseRedirect('list.html')
