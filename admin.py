#!/usr/bin/python
from atexit import register
from crypt import methods
from email import message
import json
from flask import Flask, request ,jsonify,make_response
import pymysql
from flask_cors import CORS
from sqlalchemy import true
import jwt212 
app=Flask(__name__)
CORS(app)
jwt_all=jwt212.jwt212

@app.route('/admin/del/<student_Id>',methods=["post"])##删除功能
def delete(student_Id):    
    ################################
    token=request.headers.get('token')#获取请求头中的token
    data=jwt_all.token_query(token)#获取token中的payload
    name=data.get("name")
    sql_check="SELECT password FROM user WHERE name='%s';"%(name)
   
    conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
    cursor=conn.cursor()
    cursor.execute(sql_check)
    password=cursor.fetchone()[0]##获取到密码
    cursor.close()
    conn.close()
     
    
    if jwt_all.token_check(token,password)==True and data.get("identity")=="admin":##确保签名正确且权限为admin
    ###############################################检验token的合法性##########################################################
        try:     
            if student_Id.isdigit():##检测学号是否为数字
                conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
                cursor=conn.cursor()
                sql="delete from student_view where studentId=%s;"%(student_Id)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                return {"code": 200, "data": None, "message": "成功" },200,[("Access-Control-Allow-Origin","*")]
        except Exception as e:
            print(e)
            return {"code":400, "data":None,"message":"请求失败"},400,[("Access-Control-Allow-Origin","*")]
    ###########################################################################################################
    else:
        return {"code":401,"message":"Not enough clearance"},401,[("Access-Control-Allow-Origin","*")]


@app.route('/admin/query',methods=["post"])#查询
def query():
##########################################################################################    
    token=request.headers.get('token')#获取请求头中的token
    data=jwt_all.token_query(token)#获取token中的payload
    name=data.get("name")
    sql_check="SELECT password FROM user WHERE name='%s';"%(name)
   
    conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
    cursor=conn.cursor()
    cursor.execute(sql_check)
    password=cursor.fetchone()[0]##获取到密码
    cursor.close()
    conn.close()
     
    if jwt_all.token_check(token,password)==True and data.get("identity")=="admin":##确保签名正确且权限为admin
#########################################################################################    
        dict=request.get_json()
        id=dict.get("studentId",0)
        print(id)
        if id.isdigit():
            try:    
                conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
                cursor=conn.cursor()
                sql="select * from student_view where studentId=%s"%(id)
                cursor.execute(sql)
                result=cursor.fetchone()
                cursor.close()
                conn.close()
                re_dict={"studentId":result[0],"name":result[1],"departments":result[2],"major":result[3],"address":result[4],"phone":result[5]}
                res=make_response(re_dict)
                res.status = '200' # 设置状态码
                res.headers["Access-Control-Allow-Origin"]="*"
                return res
            except Exception as e:
                print(e)
                return {"code":400, "data":None,"message":"请求失败"},400,[("Access-Control-Allow-Origin","*")]
 ######################################################################################################################   
    else:
        return {"code":401,"message":"Not enough clearance"},401,[("Access-Control-Allow-Origin","*")]


@app.route('/admin/getall',methods=["post"])#获取全部
def all():
#########################################################################################    
    token=request.headers.get('token')#获取请求头中的token
    data=jwt_all.token_query(token)#获取token中的payload
    
    name=data.get("name")
    
    sql_check="SELECT password FROM user WHERE name='%s';"%(name)
   
    conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
    cursor=conn.cursor()
    cursor.execute(sql_check)
    password=cursor.fetchone()[0]##获取到密码
    cursor.close()
    conn.close()
     
    if jwt_all.token_check(token,password)==True and data.get("identity")=="admin":##确保签名正确且权限为admin    
############################################################################################        
        try:
            conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
            cursor=conn.cursor()
            cursor.execute("select * from student_view;")
            result=cursor.fetchall()
            cursor.close()
            conn.close()
            re_list=[]
        # print(result)
            for i in result:
                re_dict={"studentId":i[0],"name":i[1],"departments":i[2],"major":i[3],"address":i[4],"phone":i[5]}
                re_list.append(re_dict)
            return json.dumps(re_list,ensure_ascii=False),200,[("Access-Control-Allow-Origin","*")]

        except Exception as e:
            print(e)
            return {"code":400, "data":None,"message":"请求失败"},400,[("Access-Control-Allow-Origin","*")]
##################################################################################################################
    else:
        return {"code":401,"message":"Not enough clearance"},401,[("Access-Control-Allow-Origin","*")]



@app.route('/admin/modify',methods=["post"])###修改
def modify():
#############################################################################
    token=request.headers.get('token')#获取请求头中的token
    data=jwt_all.token_query(token)#获取token中的payload
    
    name=data.get("name")
    
    sql_check="SELECT password FROM user WHERE name='%s';"%(name)
   
    conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
    cursor=conn.cursor()
    cursor.execute(sql_check)
    password=cursor.fetchone()[0]##获取到密码
    cursor.close()
    conn.close()
     
    if jwt_all.token_check(token,password)==True and data.get("identity")=="admin":##确保签名正确且权限为admin  

#########################################################################
        try:
            dict=request.get_json()
            #print(dict)
            id=dict.get("studentId",0)
            name=dict.get("name",0)
            departments=dict.get("departments",0)
            major=dict.get("major",0)
            print(major)
            address=dict.get("address",0)
            phone=dict.get("phone",0)
            sql="update student_view set studentId='%s',name='%s',departments='%s',major='%s',address='%s',phone='%s' where studentId='%s';"%(id,name,departments,major,address,phone,id)   
            print(sql)
            conn=pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="root",charset="utf8",db="studentall")
            cursor=conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            state={"code": 200, "data":"upgraded", "message": "成功" }
            res=make_response(state)
            res.status="200"
            res.headers["Access-Control-Allow-Origin"]="*"
            return  res
        except Exception as e:
            print(e)
            return {"code":400, "data":None,"message":"请求失败"},400,[("Access-Control-Allow-Origin","*")]
#################################################################################################################
    else:
        return {"code":401,"message":"Not enough clearance"},401,[("Access-Control-Allow-Origin","*")]

@app.route('/user/register',methods=['post'])
def register():
    dict=request.get_json()
    


if __name__=="__main__":
    app.run()