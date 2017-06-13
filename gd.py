#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
import simplejson,sys,os,urllib,re,datetime,time,hashlib,random,calendar
from django.core.handlers.wsgi import WSGIRequest
import calendar as cal
from conn import crmdb
from zz91page import *
from sphinxapi import *
from settings import searchconfig
db = crmdb()
reload(sys)
sys.setdefaultencoding('UTF-8')
nowpath=os.path.dirname(__file__)
execfile(nowpath+"/func/gd_function.py")
execfile(nowpath+"/func/crmtools.py")
zzs=zzgd()
#所有工单
def gd_list(request):
    username=request.session.get('username',default=None)
    user_id=request.session.get('user_id',default=None)
    if not username or not user_id:
        return HttpResponseRedirect("/")
    page=request.GET.get('page')
    if not page:
        page=1
    searchlist={}
    question_kind=request.GET.get("question_kind")
    if question_kind:
         searchlist['question_kind']=question_kind
    compelete=request.GET.get('compelete')
    if compelete:
         searchlist['compelete']=compelete
    index=request.GET.get('index')
    if index:
        searchlist['index']=index
    company_id=request.session.get('company_id')
    company_id=123
    if company_id:
        searchlist['company_id']=company_id
    funpage=zz91page()
    limitNum=funpage.limitNum(10)
    nowpage=funpage.nowpage(int(page))
    frompageCount=funpage.frompageCount()
    after_range_num = funpage.after_range_num(3)
    before_range_num = funpage.before_range_num(6)
    userallr=zzs.getgdlist(frompageCount=frompageCount,limitNum=limitNum,searchlist=searchlist)
    listcount=userallr['count']
    listall=userallr['list']
    index=userallr['index']
    listcount = funpage.listcount(listcount)
    page_listcount=funpage.page_listcount()
    firstpage = funpage.firstpage()
    lastpage = funpage.lastpage()
    page_range  = funpage.page_range()
    nextpage = funpage.nextpage()
    prvpage = funpage.prvpage()
    if company_id:
        return render_to_response('gd/gd_list_com.html',locals())
    else:
        return render_to_response('gd/gd_list.html',locals())
#添加工单
def gd_add(request):
    company_id=request.session.get('company_id',default=None)
    company_id=123
    if request.method=="POST":
        question=request.POST.get('question')
        question_kind=request.POST.get('question_kind')
        obj=request.FILES.get('fileField')
        if obj:
            filename=obj.name
            f=open("pic/"+filename, 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
                f.close()
        if company_id and question:
            if obj:
                sql='insert into gd_question(question,question_kind,company_id,file) values(%s, %s, %s, %s)'
                result=db.updatetodb(sql,[question,question_kind,company_id,filename])
                return HttpResponseRedirect('list_com.html')
            else:
                sql='insert into gd_question(question,question_kind,company_id) values(%s, %s, %s)'
                result=db.updatetodb(sql,[question,question_kind,company_id])
                return HttpResponseRedirect('list_com.html')
    else:
        if company_id:
            return render(request,'gd/gd_add_com.html')
        else:
            return render(request,'gd/gd_add.html')
#工单回复
def gd_answer(request):
    company_id=request.GET.get('company_id')
    question_id=request.GET.get('question_id')
    answer=request.POST.get('answer')
    obj = request.FILES.get('fileField')
    if obj:
        filename = obj.name
        f = open(filename, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
    if company_id:
        if obj:
            sql='insert into gd_answer(company_id,question_id,answer,file) values(%s, %s, %s, %s)'
            result=db.updatetodb(sql,[company_id,question_id,answer,filename])
            return HttpResponseRedirect('list_com.html')
        else:
            sql='insert into gd_answer(company_id,question_id,answer) values(%s, %s, %s)'
            result=db.updatetodb(sql,[company_id,question_id,answer])
            return HttpResponseRedirect('list_com.html')
    else:
        if obj:
            sql='insert into gd_answer(company_id,question_id,answer,file) values(0, %s, %s, %s)'
            result=db.updatetodb(sql,[question_id,answer,filename])
            return HttpResponseRedirect('list.html')
        else:
            sql='insert into gd_answer(company_id,question_id,answer) values(0, %s, %s)'
            result=db.updatetodb(sql,[question_id,answer])
            return HttpResponseRedirect('list.html')
#工单详情
def gd_details(request):
    id=request.GET.get('id')
    if id:
        #sqls='SELECT a.id,a.company_id,a.question,a.time,b.contact from ((select id,company_id,question,question_time as time from gd_question where id=%s) union (select id,company_id,answer,answer_time as time from gd_answer where question_id=%s)) as a LEFT JOIN company_account as b on a.company_id=b.company_id order by time'
        sqls='(select id,company_id,question,question_time as time from gd_question where id=%s) union (select id,company_id,answer,answer_time as time from gd_answer where question_id=%s)'
        result=db.fetchalldb(sqls,[id,id])
        result1=db.fetchonedb(sqls,[id,id])
        for list in result:
            time=list['time']
            list['time']=formattime(time,flag=2)
        company_id=request.session.get('company_id')
        company_id=123
        if company_id:
            return render_to_response('gd/gd_details_com.html',locals())
        else:
            del result1['company_id']
            return render_to_response('gd/gd_details.html',locals())
#工单状态
def gd_station(request):
    id=request.GET.get('id')
    compelete=request.GET.get('compelete')
    if id:
        sqls='update gd_question set compelete=%s where id=%s'
        result=db.updatetodb(sqls,[compelete,id])
    return HttpResponseRedirect('list_com.html')