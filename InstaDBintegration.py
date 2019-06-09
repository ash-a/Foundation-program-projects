import cx_Oracle
import datetime as dt

import os

def connection():
    conn=cx_Oracle.connect('system/ashita123$$A@localhost/system')
    return conn
def maxlikes():
    conn=connection()
    cursor=conn.cursor()
    querystring="select userid from users where username ='ashita26'"
    cursor.execute(querystring)
    id1=cursor.fetchone()
    max1=0
    picid=[]
    cursor.execute("""select pictureid from picture where userid=:param1""",{'param1':id1[0]})
    for pictureid in cursor:
        cur=conn.cursor()
       
        cur.execute("""select pictureid from likes where pictureid=:param1""",{'param1':pictureid[0]})
        cur.fetchall() 
        cur.rowcount
        if(max1==cur.rowcount):
            max1=cur.rowcount
            picid.append(pictureid[0])
        elif(max1<cur.rowcount):
            picid=[]
            max1=cur.rowcount
            picid.append(pictureid[0])
        else:
            continue
        
            
    print("pictureid")
    for p in picid:
        
        cur.execute("""select pictureid from likes where pictureid=:param1""",{'param1':p})
        for pictureid in cur.fetchmany(1):
            print("   ",pictureid[0])
    conn.commit()
    conn.close()
   
def minlikes():
    conn=connection()
    cursor=conn.cursor()
    querystring="select userid from users where username ='ashita26'"
    cursor.execute(querystring)
    id1=cursor.fetchone()
    min1=999
    picid=[]
    cursor.execute("""select pictureid from picture where userid=:param1""",{'param1':id1[0]})
    for pictureid in cursor:
        cur=conn.cursor()
        cur.execute("""select pictureid from likes where pictureid=:param1""",{'param1':pictureid[0]})
        cur.fetchall() 
        cur.rowcount
        if(min1==cur.rowcount):
            min1=cur.rowcount
            picid.append(pictureid[0])
        elif(min1>cur.rowcount and cur.rowcount!=0):
            picid=[]
            min1=cur.rowcount
            picid.append(pictureid[0])
        else:
            continue
    print("pictureid")
    for p in picid:
        cur.execute("""select pictureid from likes where pictureid=:param1""",{'param1':p})
        for pictureid in cur.fetchmany(1):
            print("   ",pictureid[0])
    conn.commit()
    conn.close()
def maxliked():
    conn=connection()
    cursor=conn.cursor()
    querystring="select userid from users where username ='ashita26'"
    cursor.execute(querystring)
    id1=cursor.fetchone()
    max1=0
    picid=[]
    cursor.execute("""select pictureid from picture where userid=:param1""",{'param1':id1[0]})
    dit={}
    for pictureid in cursor:
        cur=conn.cursor()
        cur.execute("""select pictureid from likes where pictureid=:param1""",{'param1':pictureid[0]})
        cur.fetchall() 
        picid.append(pictureid[0])
    
    cur2=conn.cursor()
    cur2.execute("select userid from users")
    for userid in cur2:
        u=userid[0]
        dit[u]=0
    for pic in picid:
        cur2=conn.cursor()
        cur2.execute("select userid from users")
        for userid in cur2:
            u=userid[0]
            cur=conn.cursor()
            cur.execute("""select pictureid from likes where userid=:param1 and pictureid=:param2""",(userid[0],pic))
            cur.fetchall()
            dit[u]=dit[u]+cur.rowcount
    print("userid")
    for key,value in sorted(dit.items(), key=lambda item: item[1],reverse=True):
        if(max1<=dit[key]):
            max1=dit[key]
            print(key)
        
    conn.commit()
    conn.close()
   
def musicpic():
    conn=connection()
    cur2=conn.cursor()
    cur2.execute("select pictureid from tags where tagname='music' or tagname='Music'")
    for pictureid in cur2:
        cur=conn.cursor()
        cur.execute("""select path from picture where pictureid=:param1""",({'param1':pictureid[0]}))
        for path in cur:
            try:  
                print(path[0])
                os.startfile(path[0])
                
            except IOError: 
                pass        
    conn.commit()
    conn.close()
def populartag():
    conn=connection()
    cursor=conn.cursor()
    max1=0
    picid=[]
    cursor.execute("select distinct lower(tagname) from tags")
    for tagname in cursor:
        
        cur=conn.cursor()
        cur.execute("""select * from tags where lower(tagname)=:param1""",{'param1':tagname[0]})
        cur.fetchall() 
        cur.rowcount
        if(max1==cur.rowcount):
            max1=cur.rowcount
            picid.append(tagname[0])
        elif(max1<cur.rowcount):
            picid=[]
            max1=cur.rowcount
            picid.append(tagname[0])
        else:
            continue   
    print("Most popular Tagname")
    for p in picid:
        print(p)
    conn.commit()
    conn.close()
def mostlikeduser():
    conn=connection()
    cur2=conn.cursor()
    dit={}
    cur2.execute("select userid from users")
    for userid in cur2:
        u=userid[0]
        dit[u]=0
        cur=conn.cursor()
        cur.execute("""select pictureid from picture where userid=:param1""",({'param1':userid[0]}))
        for pictureid in cur:
            cur3=conn.cursor()
            cur3.execute("""select pictureid from likes where pictureid=:param1""",({'param1':pictureid[0]}))
            cur3.fetchall()
            dit[u]=dit[u]+cur3.rowcount
    print("userid")
    max1=0
    for key,value in sorted(dit.items(), key=lambda item: item[1],reverse=True):
        if(max1<=dit[key]):
            max1=dit[key]
            print(key)
        
    conn.commit()
    conn.close()
   
def oldtagging():
    conn=connection()
    cursor=conn.cursor()
    querystring="select userid from users where username ='ashita26'"
    cursor.execute(querystring)
    today = dt.date.today()
    id1=cursor.fetchone()
    today2=today-dt.timedelta(days=3*365)
    cur=conn.cursor()
    tag='Old'
    cur.execute("""select pictureid from picture where userid=:param1 and picdate <=:param3""",({'param1':id1[0],'param3':today2}))
    for pictureid in cur:
        cur3=conn.cursor()
        cur3.execute("""insert into tags values(:param1,:param2)""",(pictureid[0],tag))
    print("tags updated")    
    conn.commit()
    conn.close()
def deleteinactive():
    conn=connection()
    cursor=conn.cursor()
    querystring="select userid from users"
    cursor.execute(querystring)
    today = dt.date.today()
    for userid in cursor:
        today2=today-dt.timedelta(days=365)
        cur=conn.cursor()
        cur.execute("""select userid from picture where userid=:param1 and picdate between :param2 and :param3""",({'param1':userid[0],'param2':today2,'param3':today}))
        cur.fetchall()
        if(cur.rowcount==0):
            cur3=conn.cursor()
            cur3.execute("""delete from users where userid=:param1""",({'param1':userid[0]}))
        else:
            continue
    print("users updated")    
    conn.commit()
    conn.close()
    
while True:
    print("Enter your choice\n1.Max likes\n2.Min likes\n3.Who liked most\n4.Music pictures\n5.Popilar tag\n6.Most liked user\n7.Old tagging\n8.Delete inactive users")
    choice=int(input(">>>"))
    if choice==1:
        maxlikes()
    elif(choice==2):
        minlikes()
    elif(choice==3):
        maxliked()
    elif(choice==4):
        musicpic()
    elif(choice==5):
        populartag()
    elif(choice==6):
        mostlikeduser()
    elif(choice==7):
        oldtagging()
    elif(choice==8):
        deleteinactive()
    else:
        print("Invalid choice!coming out of program")
        exit(0)
