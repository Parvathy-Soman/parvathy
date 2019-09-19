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
from urls_list import *
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
            ticketno=data["ticketNo"]
            tid=data["ticketId"]
            se=True 
            if se: 
                per = True
                if per: 
                    def stud_myprogramme(user_id):               
                        userData = requests.post(
                        stud_myprogramme_api,json={"user_id":user_id})            
                        userDataResponse=json.loads(userData.text) 
                        return userDataResponse
                    staff_list=[]
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first 
                    staff_user=UserProfile.query.filter_by(uid=user_id).first()
                    staff_fname=staff_user.fname
                    staff_lname=staff_user.lname
                    staff_details={"staff_fname":staff_fname,"staff_lname":staff_lname}
                    staff_list.append(staff_details)
                    staff_dict={"staff_details":staff_list}
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno,id=tid).first()
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
                        status_details=Complaint_reg_constants.query.filter_by(values=comp.status).first() 
                        issue_details=issue_category_constants.query.filter_by(issue_no=comp.issue_category).first()                       
                        #id1=escalation_details.
                        uid=user_details.uid
                        dasp=stud_myprogramme(uid)
                        user_programme_details=dasp["data"]
                        fname=user_details.fname
                        lname=user_details.lname
                        phone_no=user_details.phno
                        issue=issue_details.issue
                        description=comp.issue_discription
                        status=status_details.constants
                        esc_person=esl.escalated_person
                        e_date=comp.ticket_raising_date
                        date=e_date.strftime("%Y-%m-%d")
                        d={"u_id":idd,"first_name":fname,"last_name":lname,"phone":phone_no,"issue":issue,"description":description,"status":status,"escalated_person":esc_person,"ticket_raising_date":date,"id":tid,"programme_details":user_programme_details}
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
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    comp_id=comp.id
                    us_id=comp.user_id                    
                    user_details=UserProfile.query.filter_by(uid=us_id).first()
                    esl=Escalation.query.filter_by(uid=comp_id).first()
                    issue_details=issue_category_constants.query.filter_by(issue_no=comp.issue_category).first()         
                    fname=user_details.fname
                    lname=user_details.lname
                    phone_no=user_details.phno
                    issue=issue_details.issue
                    description=comp.issue_discription
                    sol=comp.solution
                    esc_person=esl.escalated_person                                  
                    l=[]
                    d={"ticket_no":ticketno,"fname":fname,"lname":lname,"phno":phone_no,"issue_discription":description,"issue_category":issue,"escalated_person":esc_person,"solution":sol}
                    
                    if comp.status==1 and esl.status==1:
                        #admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
                        comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=2))
                        esl.status=2
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
                    else:
                       return format_response(True,"already in_progress state",{})

                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
api.add_resource(Status_update,"/app/status")


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
            resolved_person=data["resolved_person"]
            # escalated_person=data["escalated_person"]
            # user_id=data["user_id"]
          
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
                    user_details=UserProfile.query.filter_by(uid=us_id).first()
                    esl=Escalation.query.filter_by(uid=comp_id).first()
                    fname=user_details.fname
                    lname=user_details.lname
                    phone_no=user_details.phno
                    issue=comp.issue_category
                    description=comp.issue_discription
                    sol=comp.solution
                    resolved_person=esl.resolved_person

                    l=[]
                    d={"ticket_no":ticketno,"lname":lname,"phno":phone_no,"issue_category":issue,"issue_discription":description,"user_id":user_id,"resolved_person":resolved_person}
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
                        sts.solution=solution
                        sts.resolved_person=resolved_person
                        # sol.status="3"
                        comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=3))
                        # sts=Escalation.query.filter_by(uid=Complaint_reg.id).update(dict(status=3))
                        sts.status=3                       
                        db.session.commit()       
                        
                    else:
                        return format_response(False,"Solution is already submitted",data)                    
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

#--------------------------------------------------------------------------------------------------
#  ticket is reassigned if the status is new(0) or reopen(5)
#--------------------------------------------------------------------------------------------------

class Ticket_assign(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']
            ticketno=data["ticketno"]
            issue=data["issue_category"]            
            ass_person=data["ass_person"]
  
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
                    l=[]
                     
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    update=Escalation.query.filter_by(uid=Complaint_reg.id).first()  
                    if comp.status==0 or comp.status==5:                                     
                        update.resolved_person=ass_person
                        db.session.commit() 
                    # else:
                    #     return format_response(True,"already in_progress state",{})
                    status=comp.status 
                    esc_person=update.escalated_person           
                    d={"ticket_no":ticketno,"issue_category":issue,"escalated_person":esc_person,"resolved_person":ass_person,"status":status}
                    data={
                            "success":"True",
                            "message":"view details",
                            "data":d                
                        }
                    l.append(d)
                    data={"staff_details":staff_list,"user_details":l}
                    return format_response(True,"view details",data)
                   
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)   
api.add_resource(Ticket_assign,"/app/assign")

#---------------------------------------------------------------------------------------------------------
#  Fetch admin and teacher for assigning the issues
#---------------------------------------------------------------------------------------------------------

class Fetch_users(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']
            se=True 
            if se: 
                per = True
                if per:
                    # def fetch_user(id):
                    #         print(id)
                        # role_details=Role.query.filter_by(id=RoleMapping.role_id).first() 
                        # admin_details=UserProfile.query.filter_by(uid=RoleMapping.user_id).first()
                        # fname=admin_details.fname
                        # lname=admin_details.lname
                        # role_id=role_details.id
                        # role_name=role_details.role_name
                        # role_type=role_details.role_type
                        # user_list=[]
                        # for i in admin_details:
                        #     uid=i.uid
                        #     fname=i.fname
                        #     lname=i.lname
                        #     phno=i.phno
                        #     d={"uid":uid,"fname":fname,"lname":lname,"phno":phno}
                        #     user_list.append(d)
                        #     return user_list
                        #     user=fetch_user(id)
                        #     details=user["data"]
                    staff_list=[]
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first 
                    staff_user=UserProfile.query.filter_by(uid=user_id).first()
                    staff_fname=staff_user.fname
                    staff_lname=staff_user.lname
                    staff_details={"staff_fname":staff_fname,"staff_lname":staff_lname}
                    staff_list.append(staff_details)
                    l=[]
                    # admin_list=[]
                    li=[]
                    user_list=[]
                    users=Role.query.all()
                    role_details=Role.query.filter_by(id=RoleMapping.role_id).first()                   
                    # admin_details=UserProfile.query.filter_by(uid=RoleMapping.user_id).first()
                    # fname=admin_details.fname
                    # lname=admin_details.lname
                    # role_id=role_details.id
                    # role_name=role_details.role_name
                    # admin_dtls={"fname":fname,"lname":lname,"id":role_id,"role_name":role_name}
                    # admin_list.append(admin_dtls)
                    # user_details=UserProfile.query.filter_by(uid=us_id)
                    # rolemap_details=RoleMapping.query.filter_by(user_id=user_details.id).first() 
                    # users=User.query.filter(id=rolemap_details.user_id)
                    # role_details=Role.query.filter_by(id=rolemap_details.role_id).first()
                  
                    for i in users:
                        if i.role_type=="Admin" or i.role_type=="Teacher":
                            r_id=i.id
                            name=i.role_name
                            role=i.role_type
                            d={"id":r_id,"role_name":name,"role":role}
                            li.append(d)                                          
                    l.append(d)
                    role_details=Role.query.filter_by(id=RoleMapping.role_id).first() 
                    admin_details=UserProfile.query.filter_by(uid=RoleMapping.user_id).first()
                    assigned_users=UserProfile.query.all()
                    fname=admin_details.fname
                    lname=admin_details.lname
                    user_list=[]
                    for i in assigned_users:
                        uid=i.uid
                        fname=i.fname
                        lname=i.lname
                            
                        d={"uid":uid,"fname":fname,"lname":lname}
                        user_list.append(d)
                    # for i in li:
                    #     rid=role_details.id
                    #     print(rid)
                    #     user=fetch_user(rid)
                    #     details=user["data"]
                        
                    #     print(i["id"])

                    data={"staff_details":staff_list,"user_details":li,"assignee_details":user_list}
                    
                    return format_response(True,"view details",data)
                    return format_response(True,"Admin details",data)    
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)   
api.add_resource(Fetch_users,"/app/users_list")






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

# class finding_assigned_persons_id(Resource): 
#     def post(self): 
#         try: 
#             data=request.get_json() 
#             user_id=data['userId'] 
#             session_id=data['sessionId'] 
#             se=True 
#             if se: 
#                 per = True 
#                 if per: 
#                     user_data=[] 
#                     role_list=[] 
#                     role=Role.query.all() 
#                     for i in role: 
#                         if i.role_type=="Admin" : 
#                             user_data.append(i.id) 
#                             user_data.append(i.role_type) 
#                             user_data.append(i.role_name) 
#                             role_list.append(user_data) 
#                             user_data=[] 
#                             elif i.role_type=="Teacher": 
#                                 user_data.append(i.id) 
#                                 user_data.append(i.role_type) 
#                                 user_data.append(i.role_name) 
#                                 role_list.append(user_data) 
#                                 user_data=[] 
#                                 return(role_list) 
#                                 else: 
#                                     return format_response(False,"Forbidden access",{},403) 
#                                     else: 
#                                         return format_response(False,"Unauthorised access",{},401) 
#                                         except Exception as e: 
#                                             print(e) 
#                                             return format_response(False,"Bad gateway",{},502)


            



               

# class StudMyProgramme(Resource):
#     def post(self):
#         try:
#             data=request.get_json()
#             user_id=data['userId']
#             session_id=data['sessionId']
            
#             se=checkSessionValidity(session_id,user_id)
#             if se:
#                 response=stud_myprogramme(user_id)
#                 return response    
#             else:
#                 return format_response(False,"Unauthorised access",{},401)
#         except Exception as e:
#             return format_response(False,"Bad gateway",{},502)
# api.add_resource(StudMyProgramme, '/app/stud_myprogramme_list')









# if __name__ == '__main__':
#     db.create_all()
#     application.run(debug = True) 
    # application.debug==True
    # application.run() 