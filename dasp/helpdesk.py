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
from session_permission import *
from dateutil import tz
to_zone=tz.gettz('Asia/Calcutta')
from datetime import datetime as dt
from collections import OrderedDict 
# api = Api(application) 

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
            # tid=data["ticketId"]
            se=checkSessionValidity(session_id,user_id)  
            
            if se: 
                per = True
                if per: 
                    def stud_myprogramme(user_id):               
                        userData = requests.post(
                        stud_myprogramme_api,json={"user_id":user_id})            
                        userDataResponse=json.loads(userData.text) 
                        return userDataResponse
                    user_data=db.session.query(Complaint_reg,Escalation,UserProfile).with_entities(Escalation.escalated_person.label("esc_person"),Escalation.resolved_person.label("res_person"),
                        Escalation.status.label("status"),Escalation.solution.label("solution"),UserProfile.uid.label("user_id"),UserProfile.fname.label("fname"),
                        UserProfile.lname.label("lname")).filter(Escalation.complaint_id==Complaint_reg.id,Escalation.resolved_person==UserProfile.uid).all()
                    userData=list(map(lambda n:n._asdict(),user_data))
                    # return format_response(True,"Resolved_person_details",userData)
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first 
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    comp_id=comp.id
                    us_id=comp.user_id
                    l=[]
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
                        esl=Escalation.query.filter_by(complaint_id=comp_id).first()                                             
                        status_details=Complaint_reg_constants.query.filter_by(values=comp.status).first() 
                        issue_details=issue_category_constants.query.filter_by(issue_no=comp.issue_category).first()  
                        # d=UserProfile.query.filter_by(uid=esl.escalated_person).first()                  
                        uid=user_details.uid
                        dasp=stud_myprogramme(uid)
                        user_programme_details=[]
                        user_programme_details.append(dasp["data"])
                        # user_programme_details=dasp["data"]
                        fname=user_details.fname
                        lname=user_details.lname
                        phone_no=user_details.phno
                        issue=issue_details.issue
                        ticketno=comp.ticket_no
                        description=comp.issue_discription
                        status=status_details.constants
                        # esc_person=d.fname
                        e_date=comp.ticket_raising_date
                        date=e_date.strftime("%Y-%m-%d")
                        tid=comp.id
                        d={"u_id":uid,"first_name":fname,"last_name":lname,"phone":phone_no,"issue":issue,"description":description,"ticketno":ticketno,"status":status,"ticket_raising_date":date,"ticket_id":tid,"programme_details":user_programme_details,"Resolved_person_details":userData}
                        
                        l.append(d)
                        data={"user_details":l}
                        return format_response(True,"Ticket numbet fetched successfully",data) 
                       
                        
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
            


              

#.........................................................................................................
#  STATUS UPDATION--by clicking the solution button,the "Pending"(2) status should be updated as "In progress"(3)
#..........................................................................................................
class Status_update(Resource):
    def post(self):
        try:
            
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']             
            ticketno=data["ticketNo"] 
            se=True 
            if se: 
                per = True
                if per:                     
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first()                    
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()                   
                    
                    if comp.status==2:                        
                        comp=Complaint_reg.query.filter_by(ticket_no=ticketno).update(dict(status=3))
                        
                        db.session.commit()                   
                       
                        return format_response(True,"Status updated successfully",{})
                        
                    else:
                       return format_response(False,"Already in progress state",{},404)

                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)



#-----------------------------------------------------------------------------------------------------------
# After writing the solution, the status "In progress"(3) should be updated as "Resolved"(4)
#---------------------------------------------------------------------------------------------------------------
                    
class Solution_confirmation(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            ticketno=data["ticketNo"]
            solution=data["solution"]
            se=True 
            if se: 
                per = True
                if per:
                    staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first() 
                    comp=Complaint_reg.query.filter_by(ticket_no=ticketno).first()                    
                    sol=Complaint_reg.query.filter_by(ticket_no=ticketno).first()
                    print(sol)
                    if sol!=None:
                        sts=Escalation.query.filter_by(complaint_id=sol.id).first()                            
                        if sol.status==3: 
                            sol.solution=solution
                            sts.solution=solution
                            sts.resolved_date=current_datetime()                           
                            sol.status=4  
                            sts.status=4                                                  
                            db.session.commit()                   
                            return format_response(True,"Solution is submitted successfully",{})
                        else:
                            return format_response(False,"Ticket number is not in progress state",{},404)  
                    else:
                        return format_response(False,"Ticket number is not available",{},404)               
                   
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
# api.add_resource(Solution_confirmation,"/app/solution")

#--------------------------------------------------------------------------------------------------
#  ticket is reassigned if the status is Resolved(4)
#--------------------------------------------------------------------------------------------------

class Ticket_reassign(Resource):
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
                    update=Escalation.query.filter_by(complaint_id=Complaint_reg.id).first()  
                    if comp.status==1 or comp.status==4:                                     
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
# api.add_resource(Ticket_reassign,"/app/re_assign")


#---------------------------------------------------------------------------------------------------------
#  Fetch admin and teacher for assigning the issues
#---------------------------------------------------------------------------------------------------------

class Assign_users(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId']             
            role=data['role']
            se=checkSessionValidity(session_id,user_id) 
            if se: 
                per = True
                if per:
                    user_list=[]
                    # staff_session=Session.query.filter_by(uid=user_id,session_token=session_id).first()
                    user_data=db.session.query(Role,RoleMapping,UserProfile).with_entities(UserProfile.uid.label("uid"),UserProfile.fname.label("fname"),UserProfile.lname.label("lname")).filter(Role.role_type==role,Role.id==RoleMapping.role_id,RoleMapping.user_id==UserProfile.uid).all()
                    userData=list(map(lambda n:n._asdict(),user_data))
                    userDetails=OrderedDict((frozenset(item.items()),item) for item in userData).values()
                    for i in userDetails:
                        dic={"userId":i.get("uid"),"fName":i.get("fname"),"lName":i.get("lname")}
                        user_list.append(dic)
                    # print(userDetails)
                    # userd=json.dumps(userDetails)
                    # user_l=json.loads(userd,object_pairs_hook=collections.OrderedDict)
                    # us=list(userDetails.items())
                    # return {"status":200,"message":userData}
                    return format_response(True,"Assignee list successfully fetched",{"assignee_list":user_list})
                
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)

def current_datetime():
    c_date=datetime.now().astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
    cur_date=dt.strptime(c_date, '%Y-%m-%d %H:%M:%S')
    return cur_date

class Assign_submit(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            uid=data["uId"]
            # escalated_person=data["escalatedPerson"]
            resolved_person=data["resolvedPerson"]
            # assigned_date=current_datetime()
            # print(resolved_date)
            # resolved_date=data["resolvedDate"]
            # status=data["status"]
            # solution=data["solution"]
            se=checkSessionValidity(session_id,user_id) 
            if se: 
                per = True
                if per:                  
                    assign=Escalation(complaint_id=uid,resolved_person=resolved_person,escalated_person=user_id)
                    comp=Complaint_reg.query.filter_by(id=uid).update(dict(status=2))
                    db.session.add(assign)
                    db.session.commit()
                    # details={"userDetails":assign}
                    # data={
                    #         "success":"True",
                    #         "message":"view details",
                    #         "data":assign               
                    #     }
                    # return data
                    return format_response(True,"Assignee is selected successfully",{})
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e)
            return format_response(False,"Bad gateway",{},502)

class Assigned_issues(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            se=checkSessionValidity(session_id,user_id) 
            if se: 
                per = True
                if per:                  
                    issues_data=db.session.query(Complaint_reg,Escalation,Complaint_reg_constants).with_entities(Complaint_reg.ticket_no.label("ticket_no"),
                        Escalation.assigned_date.label("assigned_date"),Complaint_reg_constants.constants.label("status")).filter(Escalation.resolved_person==user_id,Complaint_reg.id==Escalation.complaint_id,Complaint_reg_constants.values==Escalation.status).all()
                    issueData=list(map(lambda n:n._asdict(),issues_data))    
                    return format_response(True,"view details",issueData)
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401)
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)


class AllComp(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            status=data['status'] 
            issue_date=data['iss_date'] 
            se=checkSessionValidity(session_id,user_id) 
            if se: 
                per = True
                if per:
                    if issue_date==-1:                        
                        # if status in range(1,6):
                        #     ticket_data=db.session.query(Complaint_reg,Escalation).with_entities(Complaint_reg.ticket_raising_date.label("ticketRaisingDate"),Complaint_reg.id.label("compId"),Complaint_reg.solution.label("solution"),Complaint_reg.issue.label("issue"),
                        #         Complaint_reg.ticket_no.label("ticketNo"),Complaint_reg_constants.constants.label("status")).filter(Complaint_reg.status==status,Complaint_reg.id==Escalation.complaint_id,Complaint_reg_constants.values==Complaint_reg.status).all()
                        #     # print(type(ticket_data))
                        #     ticketData=list(map(lambda n:n._asdict(),ticket_data))
                        #     # print(ticketData)
                        #     for i in ticketData:                            
                        #         ticket_raising_date=i.get("ticketRaisingDate").strftime("%d-%m-%Y %H:%M:%S")
                        #         i['ticketRaisingDate']=ticket_raising_date
                        #     return {"status":200,"message":ticketData}
                        if status==7:
                            # print("status=7")
                            ticket_data=db.session.query(Complaint_reg,Escalation).with_entities(Complaint_reg.ticket_raising_date.label("ticketRaisingDate"),Complaint_reg.id.label("compId"),Complaint_reg.solution.label("solution"),Complaint_reg.issue.label("issue"),
                                Complaint_reg.ticket_no.label("ticketNo"),Complaint_reg_constants.constants.label("status")).filter(Complaint_reg.status.in_([1,4]),Complaint_reg_constants.values==Complaint_reg.status).all()
                            ticketData=list(map(lambda n:n._asdict(),ticket_data))
                            for i in ticketData:                            
                                ticket_raising_date=i.get("ticketRaisingDate").strftime("%d-%m-%Y %H:%M:%S")
                                i['ticketRaisingDate']=ticket_raising_date
                            # return {"status":200,"success":"True",
                            # "message":"Complaints fetched successfully","data":ticketData}
                            return format_response(True,"Complaints fetched successfully",{"ticketData":ticketData}) 
                        else:
                            return format_response(False,"no such status details",{},404) 

                            # ticket_data=db.session.query(Complaint_reg,Escalation).with_entities(Complaint_reg.ticket_raising_date.label("ticketRaisingDate"),Complaint_reg.id.label("compId"),Complaint_reg.solution.label("solution"),Complaint_reg.issue.label("issue"),Complaint_reg.ticket_no.label("ticketNo"),Complaint_reg.status.label("status"),Escalation.resolved_person.label("resolvedPerson"),Escalation.resolved_date.label("resolvedDate"),Escalation.solution.label("solution")).filter(Complaint_reg.status==status,Escalation.complaint_id==Complaint_reg.id).all()
                            # print(type(ticket_data))
                            # ticketData=list(map(lambda n:n._asdict(),ticket_data))
                            # print(ticketData)
                            # for i in ticketData:  
                            #     resolved_date=i.get("resolvedDate").strftime("%d-%m-%Y %H:%M:%S") 
                            #     i['resolvedDate']=resolved_date                         
                            #     ticket_raising_date=i.get("ticketRaisingDate").strftime("%d-%m-%Y %H:%M:%S")
                            #     i['ticketRaisingDate']=ticket_raising_date
                            # return {"status":200,"message":ticketData}
                    # print ("ajjjkjkkhk")
                    # ticket_data=db.session.query(Complaint_reg,Escalation).with_entities(Complaint_reg.ticket_raising_date.label("ticketRaisingDate"),Complaint_reg.id.label("compId"),Complaint_reg.solution.label("solution"),Complaint_reg.issue.label("issue"),
                    #             Complaint_reg.ticket_no.label("ticketNo"),Complaint_reg_constants.constants.label("status")).filter(Complaint_reg.status==status,Complaint_reg.ticket_raising_date==issue_date,Complaint_reg.id==Escalation.complaint_id,Complaint_reg_constants.values==Complaint_reg.status).all()
                    #         # print(type(ticket_data))
                    # ticketData=list(map(lambda n:n._asdict(),ticket_data))
                    # for i in ticketData:                           
                    #     ticket_raising_date=i.get("ticketRaisingDate").strftime("%d-%m-%Y %H:%M:%S")
                    #     i['ticketRaisingDate']=ticket_raising_date
                    # return {"status":200,"message":ticketData}   
                    # else:
                    #     print("fdjgghh")
                    #     ticket_data=db.session.query(Complaint_reg,UserProfile).with_entities(Complaint_reg.id.label("compId"),Complaint_reg.solution.label("solution"),Complaint_reg.issue.label("issue"),Complaint_reg.ticket_no.label("ticketNo"),Complaint_reg.status.label("status")).filter(Complaint_reg.status==status,Complaint_reg.ticket_raising_date==issue_date).all()
                    #     ticketData=list(map(lambda n:n._asdict(),ticket_data))
                    #     return {"status":200,"message":ticketData}
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)        

#--------------------------------------------------------------------------------------------------------------------------
#                                                    SEARCH USER
# --------------------------------------------------------------------------------------------------------------------------

class Search_user(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            email=data["email"]
            se=checkSessionValidity(session_id,user_id)  
            if se: 
                per = True
                if per: 
                    def stud_myprogramme(user_id):               
                        userData = requests.post(
                        stud_myprogramme_api,json={"user_id":user_id})            
                        userDataResponse=json.loads(userData.text) 
                        return userDataResponse
                    userr=User.query.filter_by(email=email).first()
                    if userr==None:
                        return format_response(False,"Not Found",{},404)
                    else:
                        idd=userr.id
                        user_details=UserProfile.query.filter_by(uid=idd).first()
                        uid=user_details.uid
                        dasp=stud_myprogramme(uid)
                        user_programme_details=dasp["data"]
                        fname=user_details.fname
                        lname=user_details.lname
                        address=user_details.padd1
                        phone_no=user_details.phno
                        details={"uId":idd,"firstName":fname,"lastName":lname,"address":address,"phone":phone_no,"email":email,"programmeDetails":user_programme_details}
                        return format_response(True,"user details fetched successfully",details)
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
        
#
# --------------------------------------------------------------------------------------------------------------------
#                                     COMPLAINT REGISTRATION
# --------------------------------------------------------------------------------------------------------------------

class Complaint_registration(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            uid=data["uId"]
            issue_category=data["issueCategory"]
            issue=data["issue"]
            description=data["description"]
            # file_attach=data["issue_ss_url"]
            se=checkSessionValidity(session_id,user_id) 
            if se: 
                per = True
                if per:
                    ticket_no=random.randint(1,1000000000)
                    print(ticket_no)
                    if description==-1:
                        r=Complaint_reg(issue_category=issue_category,issue=issue,issue_discription="NA",ticket_no=ticket_no,status=1,user_id=uid)
                        db.session.add(r)
                        db.session.commit()
                        d={"ticketNo":ticket_no}
                        details={"userDetails":d}
                        return format_response(True,"complaint registered",details)
                    else:
                        r=Complaint_reg(issue_category=issue_category,issue=issue,issue_discription=description,ticket_no=ticket_no,status=1,user_id=uid)
                        db.session.add(r)
                        db.session.commit()
                        d={"ticketNo":ticket_no}
                        details={"userDetails":d}
                        return format_response(True,"complaint registered",details)    
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e)
            return format_response(False,"Bad gateway",{},502)

# -----------------------------------------------------------------------------------------------------------------------------
                                # COMPLAINT REOPEN
# -----------------------------------------------------------------------------------------------------------------------------
class Complaint_Reopen(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            uid=data["uId"]
            ticket_no=data["ticketNo"]
            se=checkSessionValidity(session_id,user_id)
            if se: 
                per = True
                if per:
                    reopen=Complaint_reg.query.filter_by(user_id=uid,status=4,ticket_no=ticket_no).first()
                    status=reopen.status
                    ticket_no=reopen.ticket_no
                    reopen.status=6
                    db.session.commit()
                    details={"ticketNo=":ticket_no}
                    return format_response(True,"complained reopened",details)       
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            return format_response(False,"Bad gateway",{},502)
# -------------------------------------------------------------------------------------------------------------------
#                                   PREVIOUS COMPLAINTS-SAME USER
# -------------------------------------------------------------------------------------------------------------------        
class Complaint_previous(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            uid=data["uId"]
            se=checkSessionValidity(session_id,user_id)
            if se: 
                per = True
                if per:
                    def previ(id):
                        try:
                            l1=[]
                            previous_est=Escalation.query.filter_by(complaint_id=id).first()
                            escalated_person=previous_est.escalated_person
                            l1.append(escalated_person)
                            resolved_person=previous_est.resolved_person
                            l1.append(resolved_person)
                            return l1
                        except Exception:
                            l1=[]
                            escalated_person="NA"
                            l1.append(escalated_person)
                            resolved_person="NA"
                            l1.append(resolved_person)
                            return l1
                    previous=Complaint_reg.query.filter_by(user_id=uid).all()
                    previous_len=len(previous)
                    if previous_len==0:
                        return format_response(False,"no previous complaints",{},404) 
                    else:
                        details_list=[]
                        l1=[]
                        for i in previous:
                            id=i.id
                            issue_category=i.issue_category
                            issue_check=issue_category_constants.query.filter_by(issue_no=issue_category).first()
                            issue_category=issue_check.issue
                            issue_discription=i.issue_discription
                            issue=i.issue
                            if issue==None:
                                issue="NA"
                            ticket_no=i.ticket_no
                            ticket_raising_date=i.ticket_raising_date
                            ticket_raising_date=ticket_raising_date.strftime("%d-%m-%Y %H:%M:%S")
                            solution=i.solution
                            status=i.status
                            status_check=Complaint_reg_constants.query.filter_by(values=status).first()
                            status=status_check.constants
                            es_previous=previ(id)
                            escalated_person=es_previous[0]
                            resolved_person=es_previous[1]
                            d={"issueCategory" :issue_category,"issueDiscription":issue_discription,"issue":issue,"ticketNo":ticket_no,"ticketRaisingDate":ticket_raising_date,"solution":solution,"status":status,"escalatedPerson":escalated_person,"resolvedPerson":resolved_person}
                            details_list.append(d)
                        details={"userDetails":details_list}
                        return format_response(True,"view details",details)  
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
#   -----------------------------------------------------------------------------------------------------------------
#                                 ALL COMPLAINTS-ALL USER
#   -----------------------------------------------------------------------------------------------------------------              




class All_complaints(Resource):
     def post(self):
        try:
            data=request.get_json()
            user_id=data['userId'] 
            session_id=data['sessionId'] 
            print(data)
            # status=data['status'] 
            se=checkSessionValidity(session_id,user_id) 
            se=True
            if se: 
                per = True
                if per:
                    def previous(id):
                        try:
                            l1=[]
                            previous_est=Escalation.query.filter_by(complaint_id=id).first()
                            escalated_person=previous_est.escalated_person
                            l1.append(escalated_person)
                            resolved_person=previous_est.resolved_person
                            l1.append(resolved_person)
                            return l1
                        except Exception:
                            l1=[]
                            escalated_person="NA"
                            l1.append(escalated_person)
                            resolved_person="NA"
                            l1.append(resolved_person)
                            return l1
                    previous_comp=Complaint_reg.query.all()
                    if previous_comp==None:
                        return format_response(False,"no results found",{},404) 
                    details_list=[]
                    l1=[]
                    for i in previous_comp:
                        id=i.id
                        issue_category=i.issue_category
                        issue_discription=i.issue_discription
                        issue=i.issue
                        issue_check=issue_category_constants.query.filter_by(issue_no=issue_category).first()
                        issue_category=issue_check.issue
                        ticket_no=i.ticket_no
                        ticket_raising_date=i.ticket_raising_date
                        ticket_raising_date=ticket_raising_date.strftime("%d-%m-%Y %H:%M:%S")
                        solution=i.solution
                        status=i.status
                        status_check=Complaint_reg_constants.query.filter_by(values=status).first()
                        status=status_check.constants
                        es_previous=previous(id)
                        escalated_person=es_previous[0]
                        resolved_person=es_previous[1]
                        d={"issueCategory" :issue_category,"issueDiscription":issue_discription,"ticketNo":ticket_no,"ticketRaisingDate":ticket_raising_date,"solution":solution,"status":status,"escalatedPerson":escalated_person,"resolvedPerson":resolved_person}
                        details_list.append(d)
                    details={"userDetails":details_list}
                    return format_response(True,"view details",details)  
                else: 
                    return format_response(False,"Forbidden access",{},403) 
            else: 
                return format_response(False,"Unauthorised access",{},401) 
        except Exception as e:
            print(e) 
            return format_response(False,"Bad gateway",{},502)
              



            



               

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