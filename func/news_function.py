#-*- coding:utf-8 -*-
class zznews:
    def __init__(self):
        self.db=db
#所有数据
    def getnewslist(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        sqls=""
        star=searchlist.get("star")
        if star:
            sqls+=" and star=%s"
            argument.append(star)
        sqlcount="select count(0) as count from bz_article"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select aid,subject,hit from bz_article where aid>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
