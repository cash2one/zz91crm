#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,md5,hashlib,random,calendar
import calendar as cal
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db = crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/seo_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzseo()


def seo_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    if not page:
        page=1
        
    searchlist={}
    com_email=request.GET.get("com_email")
    if com_email:
        searchlist['com_email']=com_email
    
    com_msb=request.GET.get("com_msb")
    if com_msb:
        searchlist['com_msb']=com_msb
    
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getseolist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    return render_to_response('seo/seo_list.html',locals())    

def seo_add(request):
    com_id=request.POST.get('com_id')
    com_email=request.POST.get('com_email')
    com_msb=request.POST.get('com_msb')
    price=request.POST.get("price")
    baidu_sl=request.POST.get('baidu_sl')
    baidu_fanlian=request.POST.get('baidu_fanlian')
    personid=request.POST.get('personid')
    if com_id:
        sql='insert into seo_list(com_id, com_email,com_msb, price,baidu_sl,baidu_fanlian,personid) values(%s, %s, %s,%s, %s, %s,%s)'
        result=db.updatetodb(sql,[com_id, com_email,com_msb, price,baidu_sl,baidu_fanlian,personid])
        return HttpResponseRedirect('list.html')
    return render(request,'seo/seo_add.html')

def seo_del(request):
    id=request.GET.get('id')
    if id:
        sql='delete from seo_list where id=%s'
        result=db.updatetodb(sql,[id])
        return HttpResponseRedirect('list.html')
            
def seo_mod(request):
    if request.method=='POST':
        com_id=request.POST.get('com_id')
        com_email=request.POST.get('com_email')
        com_msb=request.POST.get('com_msb')
        price=request.POST.get("price")
        baidu_sl=request.POST.get('baidu_sl')
        baidu_fanlian=request.POST.get('baidu_fanlian')
        personid=request.POST.get('personid')
        id=request.GET.get('id')
        if com_id and com_email and com_msb and price and baidu_sl and baidu_fanlian and personid:
            sql='update seo_list set com_id=%s,com_email=%s,com_msb=%s,price=%s,baidu_sl=%s,baidu_fanlian=%s,personid=%s where id=%s'
            result=db.updatetodb(sql,[com_id,com_email,com_msb,price,baidu_sl,baidu_fanlian,personid,id])
        return HttpResponseRedirect('list.html')
    else:
        id=request.GET.get('id')
        if id:
            sql='select * from seo_list where id=%s'
            result=db.fetchonedb(sql,[id])
            return render_to_response('seo/seo_mod.html',locals())


