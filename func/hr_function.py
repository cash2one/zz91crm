class zzhr:
    def __init__(self):
        self.db=db
#所有数据
    def gethrlist(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        sqls=""
        star=searchlist.get("star")
        username=searchlist.get("username")
        mobile=searchlist.get("mobile")
        email=searchlist.get("email")
        sex=searchlist.get("sex")
        jl1=searchlist.get("jl1")
        jl2=searchlist.get("jl2")
        jl3=searchlist.get("jl3")
        jl4=searchlist.get("jl4")
        jl5=searchlist.get("jl5")
        personid=searchlist.get("personid")
        rpersonid=searchlist.get("rpersonid")
        if star:
            sqls+=" and star=%s"
            argument.append(star)
        if username:
            sqls+=" and username=%s"
            argument.append(username)
        if mobile:
            sqls+=" and mobile=%s"
            argument.append(mobile)
        if email:
            sqls+="and email=%s"
            argument.append(email)
        if sex:
            sqls+=" and sex=%s"
            argument.append(sex)
        if jl1:
            sqls+=" and jl1=%s"
            argument.append(jl1)
        if jl2:
            sqls+=" and jl2=%s"
            argument.append(jl2)
        if jl3:
            sqls+=" and jl3=%s"
            argument.append(jl3)
        if jl4:
            sqls+=" and jl4=%s"
            argument.append(jl4)
        if jl5:
            sqls+=" and jl5=%s"
            argument.append(jl5)
        if personid:
            sqls+=" and personid=%s"
            argument.append(personid)
        if rpersonid:
            sqls+=" and personid3=%s"
            argument.append(rpersonid)
            sqlcount="select count(0) as count from renshi_user as a left join renshi_category as b on a.education=b.code left join user as c on c.id=a.personid left join (select personid as personid3,uid, max(id) as id from renshi_history group by uid) as d on d.uid=a.id left join user as e on d.personid3=e.id where a.id>0 "+sqls+""
        else:    
            sqlcount="select count(0) as count from renshi_user where id>0 "+sqls+""
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select personid,personid3,a.id,a.star,a.mobile,a.username,a.sex,a.education,a.interviewTime,a.station,a.jl1,a.jl2,a.jl3,a.jl4,a.jl5,a.laiyuan,a.othercontact,a.email,a.gmt_created,b.label,e.realname as realname3,c.realname from renshi_user as a left join renshi_category as b on a.education=b.code left join user as c on c.id=a.personid left join (select personid as personid3,uid, max(id) as id from renshi_history group by uid) as d on d.uid=a.id left join user as e on d.personid3=e.id where a.id>0 "+sqls+" limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}
#人事基础数据
    def gethrbasiclist(self,searchlist=""):
        argument=[]
        sqls=""
        label=searchlist.get("label")
        if label:
            sqls+="and label=%s"
            argument.append(label)
        sqllist="select * from renshi_category where id>0 "+sqls+" order by code"
        listall=db.fetchalldb(sqllist,argument)
        return {'list':listall}
#面试记录
    def getrenshihistory(self,frompageCount="",limitNum="",searchlist=""):
        argument=[]
        uid=searchlist.get("uid")
        if uid:
            argument.append(uid)
        sqlcount="select count(0) as count from renshi_history where uid=%s"
        count=db.fetchonedb(sqlcount,argument)['count']
        sqllist="select a.bz,a.nextteltime,b.label,c.realname from renshi_history as a left join renshi_category as b on a.code=b.code left join user as c on c.id=a.personid where uid=%s limit "+str(frompageCount)+","+str(limitNum)+""
        listall=db.fetchalldb(sqllist,argument)
        return {'count':count,'list':listall}