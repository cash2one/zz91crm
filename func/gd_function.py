# -*- coding: utf-8 -*-  
class zzgd:
    def __init__(self):
        self.db=db
#所有工单
    def getgdlist(self,frompageCount="",limitNum="",searchlist=""):
        sqls=""
        argument=[]
        question_kind=searchlist.get("question_kind")
        if question_kind:
            sqls+="and question_kind=%s"
            argument.append(question_kind)
        compelete=searchlist.get("compelete")
        if compelete:
            sqls+="and compelete=%s"
            argument.append(compelete)
        index=searchlist.get("index")
        if index:
            index=index
        else:
            index=1
        company_id=searchlist.get("company_id")
        if company_id:#客户登陆
            sqls+="and company_id=%s"
            argument.append(company_id)
            sqlcount="select count(0) as count from gd_question where id>0 "+sqls+""
            count=db.fetchonedb(sqlcount,argument)['count']
            sqllist="select id,question,company_id,question_time,question_kind,compelete from gd_question where id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
            listall=db.fetchalldb(sqllist,argument)
            for list in listall:
                time=list['question_time']
                list['question_time']=formattime(time,flag=2)
            return {'count':count,'list':listall}
        else:#工作人员登陆
            sqlcount="select count(0) as count from gd_question where id>0 "+sqls+""
            count=db.fetchonedb(sqlcount,argument)['count']
            sqllist="select a.id,a.question,a.company_id,a.question_time,a.question_kind,a.compelete,b.mobile,b.contact from gd_question as a LEFT JOIN company_account as b on a.company_id=b.company_id where a.id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
            listall=db.fetchalldb(sqllist,argument)
            for list in listall:
                time=list['question_time']
                list['question_time']=formattime(time,flag='1')
            return {'count':count,'list':listall,'index':index}
