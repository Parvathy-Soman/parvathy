from flask import Flask,jsonify,url_for
from flask import request
import json
import requests
import flask_restful as restful
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime
import random
from format_response import *
application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI']='mysql://user7332:*+()!Gyuiq@instancenew.ckssxhrwykga.ap-south-1.rds.amazonaws.com/dastp_mw_dev'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(application)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True) 
    email=db.Column(db.String(200),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False) 
    reg_date=db.Column(db.Date,nullable=True) 
    trans_id=db.Column(db.String(200),nullable=True)
    exp_date=db.Column(db.Date,nullable=True)
    trans_req_id=db.Column(db.String(200),nullable=True) 
    status=db.Column(db.String(200),default=0)
class Complaint_reg(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    issue_category=db.Column(db.String(100),unique=False,nullable=False)
    issue_discription=db.Column(db.String(200),unique=False,nullable=False)
    ticket_raising_date= db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    ticket_no=db.Column(db.Integer,unique=True,nullable=False)
    solution=db.Column(db.String(200),unique=False,nullable=True)
    status=db.Column(db.String(100),unique=False,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
class Escalation(db.Model): 
    id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
    escalated_person=db.Column(db.Integer,unique=False,nullable=False) 
    resolved_person=db.Column(db.Integer,unique=False,nullable=False) 
    resolved_date=db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow) 
    uid=db.Column(db.Integer,db.ForeignKey('complaint_reg.id'))
class UserProfile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    fname=db.Column(db.String(100),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    fullname=db.Column(db.String(300),nullable=True)
    phno=db.Column(db.String(100),nullable=True) 
    gender=db.Column(db.String(20),nullable=True) 
    photo=db.Column(db.String(100),nullable=True) 
    padd1=db.Column(db.String(200),nullable=True) 
    padd2=db.Column(db.String(200),nullable=True) 
    pcity=db.Column(db.String(200),nullable=True) 
    pstate=db.Column(db.String(200),nullable=True) 
    pcountry=db.Column(db.String(200),nullable=True) 
    ppincode=db.Column(db.String(200),nullable=True) 
    madd1=db.Column(db.String(200),nullable=True) 
    madd2=db.Column(db.String(200),nullable=True) 
    mcity=db.Column(db.String(200),nullable=True) 
    mstate=db.Column(db.String(200),nullable=True) 
    mcountry=db.Column(db.String(200),nullable=True) 
    mpincode=db.Column(db.String(200),nullable=True) 
    religion=db.Column(db.String(200),nullable=True) 
    caste=db.Column(db.String(200),nullable=True) 
    nationality=db.Column(db.String(200),nullable=True) 
    dob=db.Column(db.DateTime,nullable=True) 
    s_caste=db.Column(db.String(200),nullable=True) 
    annualincome=db.Column(db.String(100),nullable=True) 
    aadhar=db.Column(db.String(50),nullable=True)
    
class Search_ticket(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticketno=data["ticketno"]
            se=True 
            if se: 
                per = True
                if per: 
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    comp_id=comp.id
                    us_id=comp.user_id
                    #return id1
                    data1={
                    "success":"False",
                    "message":"Ticket number is not available"
                    }
                    if comp==None:
                        return data1
                    else:
                        idd=comp.id
                        #return idd                              
                        user_details=UserProfile.query.filter_by(uid=us_id).first()
                        esl=Escalation.query.filter_by(uid=comp_id).first()
                        #id1=escalation_details.
                        fname=user_details.fname
                        lname=user_details.lname
                        phone_no=user_details.phno
                        issue=comp.issue_category
                        description=comp.issue_discription
                        status=comp.status
                        esc_person=esl.escalated_person
                        e_date=comp.ticket_raising_date
                        date=e_date.strftime("%Y-%m-%d")
                        d={"u_id":idd,"first_name":fname,"last_name":lname,"phone":phone_no,"issue":issue,"description":description,"status":status,"escalated_person":esc_person,"ticket_raising_date":date}
                        data2={
                        "success":"True",
                        "message":"view details",
                        "data":d
                        }
                        return data2
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
                
api.add_resource(Search_ticket,"/app/ticket_search")

class Status_update(Resource):
    def post(self):
        try:
            
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']             
            ticketno=data["ticketno"] 
            #comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()           
            fname=data["fname"]
            lname=data["lname"]
            phone_no=data["phno"]
            issue=data["issue"]
            description=data["discription"]
            esc_person=data["escalated_person"]
            sol=data["solution"]
            status=data["status"]
            se=True 
            if se: 
                per = True
                if per: 
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    
                    d={"ticket_no":ticketno,"fname":fname,"lname":lname,"phno":phone_no,"issue_discription":description,"issue_category":issue,"escalated_person":esc_person,"solution":sol,"status":status}
                    
                    if comp.status=="pending":
                        #admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
                        comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status="In progress"))
                        db.session.commit()
                        
                        # status=com.status
                        # s={"status":status}
                        # return s
            
                        # if sol=="":
                        #     api.add_resource(Update_issue,"/app/update")
                        data={
                            "success":"True",
                            "message":"view details",
                            "data":d
                        }
                      
                        return data
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
api.add_resource(Status_update,"/app/status")

class Search_user(Resource):
    def post(self): 
        data=request.get_json() 
        print(data)
        email=data["email"] 
        userr=User.query.filter_by(email=email).first() 
        data1={ 
        "success":"False", 
        "message":"not registered user" 
        } 
        if userr==None: 
            return data1 
        else: 
            idd=userr.id 
            user_details=UserProfile.query.filter_by(uid=idd).first() 
            fname=user_details.fname 
            lname=user_details.lname 
            address=user_details.padd1 
            phone_no=user_details.phno 
            d={"u_id":idd,"first_name":fname,"last_name":lname,"address":address,"phone":phone_no,"email":email} 
            data2={                                        
            "success":"True", 
            "message":"view details", 
            "data":d 
            }         
            return data2 
api.add_resource(Search_user,"/app/search")

class Update_issue(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticketno=data["ticketno"]
            solution=data["solution"]
            status=data["status"]
            se=True 
            if se: 
                per = True
                if per: 
                    update=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    data1={        
                        "success":"False",
                        "message":"Updation failed"            
                    }
                    if update==None: 
                        return data1 
                    else: 
                        update.solution=solution
                        update.status=status
                        db.session.commit()
                        
                    data2={
                        "success":"True",
                        "message":"Details updated successfully" 
                    }
                    return data2
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
api.add_resource(Update_issue,"/app/update")

class Solution_confirmation(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticketno=data["ticketno"]
            fname=data["fname"]
            lname=data["lname"]
            issue=data["issue"]
            solution=data["solution"]
            discription=data["discription"]
            user_id=data["user_id"]
            se=True 
            if se: 
                per = True
                if per:
                    d={"ticket_no":ticketno,"fname":fname,"lname":lname,"issue_category":issue,"solution":solution,"issue_discription":discription,"user_id":user_id}
                    sol=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    # db.session.add(sol)
                    # db.session.commit()
                    data1={        
                        "success":"False",
                        "message":"Updation failed"            
                    }
                    if sol==None: 
                        return data1 
                    else:
                        sol.solution=solution
                        db.session.commit()                     
                    data2={
                        "success":"True",
                        "message":"view details",
                        "data":d
                        }
                    return data2
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
                    
api.add_resource(Solution_confirmation,"/app/solution")

class Solution_submit(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticket=data["ticketno"]
            issue=data["issue"]
            des=data["discription"]
            sol=data["solution"]
            res_person=data["resolved_person"]
            se=True 
            if se: 
                per = True
                if per:
                    d={"ticket_no":ticket,"issue_discription":des,"issue_category":issue,"solution":sol,"resolved_person":res_person}
                    data={
                            "success":"True",
                            "message":"view details",
                            "data":d                
                        }
                    return data
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)    
api.add_resource(Solution_submit,"/app/submit")
            
class student_login(Resource): 
    def post(self): 
        data=request.get_json() 
        uid=data["user_id"] 
        status=data["status"] 
        #print(type(status)) 
        update=Complaint_reg.query.filter_by(user_id=uid).first()
        if status=="resolved":
            update=Complaint_reg.query.filter_by(user_id=uid).update(dict(status="Pending"))
            db.session.commit() 
            #print(update.status) 
            #print(type(update.status)) 
            data1={ "Message":"update failed", } 
            data2={ "Message":"update success", } 
            if update==None: 
                return data1 
            else:                              
                return data2 
api.add_resource(student_login,"/app/log")

# class Complaint_registration(Resource):
#     def post(self):
#             data=request.get_json()
#             name=data["name"]
#             phone=data["phone"]
#             user_id=data["user_id"]
#             issue=data["issue"]
#             description=data["description"]
#             d={"name":name,"phone":phone,"user_id":user_id,"issue":issue,"description":description}
#             data1={
#                 "success":"True",
#                 "message":"view details",
#                 "data":d
#             }
#             return data1
# api.add_resource(Complaint_registration,"/app/com_reg")
# class Complaint_conformation(Resource):
#     def post(self):
#             data=request.get_json()
#             issue=data["issue"]
#             description=data["description"]
#             ticket_no=random.randint(1,1000000000)
#             user_id=data["user_id"]
#             r=Complaint_reg(issue_category=issue,issue_discription=description,ticket_no=ticket_no,status="pending",user_id=user_id)
#             db.session.add(r)
#             db.session.commit()
#             d={"ticket_no":ticket_no}
#             data2={
#                 "success":"True",
#                 "message":"view details",
#                 "data":d
#                 }
#             return data2
# api.add_resource(Complaint_conformation,"/app/complaint")




# class sample(Resource):
#     def post(self):
#         data=request.get_json()
#         email=data["email"]
#         userr=User.query.filter_by(email=email).first()
#         data1={
#             "success":"False",
#             "message":"not registered user"
#         }
#         if userr==None:
#             return data1
#         else:
#             def dasp(idd): 
#                 userData = requests.post(dasp_helpdeskk,json={"user_id":idd}) 
#                 userDataResponse=json.loads(userData.text) 
#                 return userDataResponse
#             idd=userr.id
#             user_details=UserProfile.query.filter_by(uid=idd).first()
#             fname=user_details.fname
#             lname=user_details.lname
#             address=user_details.padd1
#             phone_no=user_details.phno
#             var=dasp(idd)
#             return var
#             d={"u_id":idd,"first_name":fname,"last_name":lname,"address":address,"phone":phone_no}
#             data2={
#             "success":"True",
#             "message":"view details",
#             "data":d
#             }
#             return data2
    
# dasp_helpdeskk="http://192.168.0.1/api/gateway/dasp_helpdesk"
# api.add_resource(sample,"/app/conn")

# try: 
#     data=request.get_json() 
#     user_id=data['userId'] 
#     session_id=data['sessionId'] 
#     exam_id=data['examId'] 
#     prgm_id=data['programmeId'] 
#     course_id=data['courseId'] 
#     total_mark=data["totalMark"] 
#     qp_type=data["qpType"] 
#     qp_count=data["qpCount"] 
#     question_count=data["questionCount"] 
#     duration=data['examDuration'] 
#     se=checkSessionValidity(session_id,user_id) 
#     if se: 
#         per = checkapipermission(user_id, self.__class__.__name__) 
#         if per: 
#             questionObj=db.session.query(QuestionBank,UserProfile,User,QuestionOwner).with_entities(UserProfile.fname.label("fname"),UserProfile.lname.label("lname"),QuestionBank.question.label("question"),QuestionBank.options.label("options"),QuestionBank.unit.label("unit"),QuestionBank.answer.label("answer"),QuestionBank.mark.label("mark"),QuestionBank.diff_level.label("diffLevel"),QuestionBank.qustn_img.label("questionImage"),QuestionOwner.user_id.label("userId"),QuestionBank.option_img.label("option_img"),QuestionBank.status.label("status")).filter(QuestionBank.status=="pending",QuestionBank.prgm_id==prgm_id,QuestionBank.course_id==course_id,User.id==QuestionOwner.user_id,QuestionOwner.question_id==QuestionBank.question_id,UserProfile.uid==User.id).all() questionDet=list(map(lambda n:n._asdict(),questionObj)) 
#             if questionDet==[]: 
#                 return format_response(False,"There is no questions for approval",{},404) 
#             else: 
#                 for i in questionDet: 
#                     option=i.get("options") 
#                     res = ast.literal_eval(option) 
#                     i["options"]=res 
#                     return format_response(True,"Successfully fetched",questionDet) 
#         else: 
#             return format_response(False,"Forbidden access",{},403) 
#     else: 
#         return format_response(False,"Unauthorised access",{},401) 
# except Exception as e: 
#     return format_response(False,"Bad gateway",{},502)

if __name__ == '__main__':
    db.create_all()
    application.run(debug = True) 
    # application.debug==True
    # application.run() 