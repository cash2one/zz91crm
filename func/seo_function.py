# -*- coding: utf-8 -*-  
class zzseo:
    def __init__(self):
        self.db=db
#所有记录
    def getseolist(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        sqls=""
        com_email=searchlist.get("com_email")
        com_msb=searchlist.get("com_msb")
        if com_email:
            sqls+=" and com_email=%s"
            argument.append(com_email)
        if com_msb:
            sqls+=" and com_msb=%s"
            argument.append(com_msb)
        sqlcount="select count(0) as count from seo_list where id>0 "+sqls+""
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select a.id,a.com_id,a.com_email,a.com_msb,a.price,a.baidu_sl,a.baidu_fanlian,a.personid from seo_list as a where id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        for list in listall:
            sid=list['id']
            sqls="select b.sid,b.keywords,b.baidu_ranking,b.target_require,b.expire_time,b.price,b.gmt_created from seo_keywordslist as b where sid=%s"
            lists=db.fetchalldb(sqls,[sid])
            list['keywordslist']=lists
        return {'count':count,'list':listall}
