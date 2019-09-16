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
from model import *

api = Api(application) 

#--------------------------------------------------------------------------------------------------------
# Ticket is searched based on ticket number
#---------------------------------------------------------------------------------------------------------
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
                    staff_list=[]
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first 
                    staff_user=UserProfile.query.filter_by(uid=user_id).first()
                    staff_fname=staff_user.fname
                    staff_lname=staff_user.lname
                    staff_details={"staff_fname":staff_fname,"staff_lname":staff_lname}
                    staff_list.append(staff_details)
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    comp_id=comp.id
                    us_id=comp.user_id
                    l=[]
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
                        # data2={
                        # "success":"True",
                        # "message":"view details",
                        # "data":d
                        # }
                        l.append(d)
                        data={"staff_details":staff_list,"user_dtatils":l}
                        return format_response(True,"view details",data) 
                        # return data2
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)

api.add_resource(Search_ticket,"/app/ticket_search")                

#.........................................................................................................
#  STATUS UPDATION--by clicking the solution button,the "Pending"(1) status should be updated as "In progress"(2)
#..........................................................................................................
class Status_update(Resource):
    def post(self):
        try:
            
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']             
            ticketno=data["ticketno"] 
            #comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()           
            # fname=data["fname"]
            # lname=data["lname"]
            # phone_no=data["phno"]
            # issue=data["issue"]
            # description=data["discription"]
            # esc_person=data["escalated_person"]
            # sol=data["solution"]
            # status=data["status"]
            se=True 
            if se: 
                per = True
                if per: 
                    staff_list=[]
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first 
                    staff_user=UserProfile.query.filter_by(uid=user_id).first()
                    staff_fname=staff_user.fname
                    staff_lname=staff_user.lname
                    staff_details={"staff_fname":staff_fname,"staff_lname":staff_lname}
                    staff_list.append(staff_details)
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno,status=1).first()
                    comp_id=comp.id
                    us_id=comp.user_id                    
                    user_details=UserProfile.query.filter_by(uid=us_id).first()
                    esl=Escalation.query.filter_by(uid=comp_id).first()
                    fname=user_details.fname
                    lname=user_details.lname
                    phone_no=user_details.phno
                    issue=comp.issue_category
                    description=comp.issue_discription
                    sol=comp.solution
                    esc_person=esl.escalated_person                                  
                    l=[]
                    d={"ticket_no":ticketno,"fname":fname,"lname":lname,"phno":phone_no,"issue_discription":description,"issue_category":issue,"escalated_person":esc_person,"solution":sol}
                    
                    # if comp.status==1:
                        #admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=2))
                    db.session.commit()                   
                    data={
                            "success":"True",
                            "message":"view details",
                            "data":d
                    }
                    l.append(d)
                    data={"staff_details":staff_list,"user_dtatils":l}
                    return format_response(True,"view details",data)
                        # return data
                    # else:
                    #     return format_response(True,"already in_progress state",{})

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

#--------------------------------------------------------------------------------------------------------
#
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




#-----------------------------------------------------------------------------------------------------------
# After writing the solution, the status "In progress"(2) should be updated as "Resolved"(3)
#---------------------------------------------------------------------------------------------------------------
                    
class Solution_confirmation(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticketno=data["ticketno"]
            # fname=data["fname"]
            # lname=data["lname"]
            # issue=data["issue"]
            solution=data["solution"]
            # discription=data["discription"]
            # res_person=data["resolved_person"]
            # user_id=data["user_id"]
          
            se=True 
            if se: 
                per = True
                if per:
                    staff_list=[]
                    staff_user=UserProfile.query.filter_by(uid=user_id,id=session_id).first()
                    staff_fname=staff_user.fname
                    staff_lname=staff_user.lname
                    staff_details={"staff_fname":staff_fname,"staff_lname":staff_lname}
                    staff_list.append(staff_details)
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    comp_id=comp.id
                    us_id=comp.user_id                    
                    user_details=UserProfile.query.filter_by(uid=us_id).first()
                    esl=Escalation.query.filter_by(uid=comp_id).first()
                    fname=user_details.fname
                    lname=user_details.lname
                    phone_no=user_details.phno
                    issue=comp.issue_category
                    description=comp.issue_discription
                    sol=comp.solution
                    l=[]
                    d={"ticket_no":ticketno,"lname":lname,"phno":phone_no,"issue_category":issue,"issue_discription":description,"user_id":user_id}
                    sol=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    sts=Escalation.query.filter_by(uid=Complaint_reg.id).first()
                    # comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=3))
                    # db.session.add(sol)
                    # db.session.commit()
                    # data={        
                    #     "success":"False",
                    #     "message":"Updation failed"            
                    # }
                    if sol.status==2 and sts.status==2:
                        sol.solution=solution
                        sts.status=solution
                        # sol.status="3"
                        comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=3))
                        # sts=Escalation.query.filter_by(uid=Complaint_reg.id).update(dict(status=3))
                        sts.status=3
                        db.session.commit()       
                        
                    else:
                        return data                    
                    data={
                        "success":"True",
                        "message":"view details",
                        "data":d
                        }
                    l.append(d)
                    data={"staff_details":staff_list,"user_details":l}
                    return format_response(True,"view details",data)
                    # return data2
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

class Ticket_assign(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']
            ticketno=data["ticket_no"]
            name=data["fname"]
            issue=data["issue"]
            discription=data["discription"]
            esc_person=data["esc_person"]
            ass_person=data["ass_person"]
            se=True 
            if se: 
                per = True
                if per:
                    update=Escalation.query.filter_by(uid=Complaint_reg.id).first()
                    update.resolved_person=ass_person
                    db.session.commit()
                    d={"ticket_no":ticketno,"fullname":name,"issue_category":issue,"issue_discription":discription,"escalated_person":esc_person,"assigned_person":ass_person}
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


class Complaint_conformation(Resource): 
    def post(self): 
        
        data=request.get_json() 
        userid=data['userId'] 
        session_id=data['sessionId'] 
        uid=data["userid"] 
        issue=data["issue"] 
        description=data["description"] 
           
        comp=Complaint_reg.query.filter_by(user_id=uid).first() 
                    
        d={"user_id":uid,"issue":issue,"discription":description}
        #return d
                    
        if comp.status=="Pending":
                        #admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
            comp=Complaint_reg.query.filter_by(user_id=uid).update(dict(status="In progress"))
            db.session.commit()
            data={
                "success":"True",
                "message":"view details",
                "data":d        
            }
                      
            return data
                    # update=comp_previous.status
                    #db.session.commit() 
                    #return format_response(True,"complained reopened",d) 
                        #except Exception: 
                    # ticket_no=random.randint(1,1000000000) 
                    # r=Complaint_reg(issue_category=issue,issue_discription=description,ticket_no=ticket_no,status=update,user_id=uid) 
                    # update.status="new"
                    # db.session.add(r) 
                    # db.session.commit() 
                    # d={"ticket_no":ticket_no} 
                       
                    #return format_response(True,"complained registered",d) 
               








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

# if __name__ == '__main__':
#     db.create_all()
#     application.run(debug = True) 
    # application.debug==True
    # application.run() 