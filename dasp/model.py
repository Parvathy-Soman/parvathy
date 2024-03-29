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
    ticket_raising_date= db.Column(db.Date(), default=datetime.utcnow, onupdate=datetime.utcnow)
    ticket_no=db.Column(db.Integer,unique=True,nullable=False)
    solution=db.Column(db.String(200),unique=False,nullable=True)
    status=db.Column(db.Integer,unique=False,nullable=False)
    issue=db.Column(db.String(200),unique=False,nullable=False)
    issue_ss_url=db.Column(db.String(200),unique=False,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
class Escalation(db.Model): 
    id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
    escalated_person=db.Column(db.Integer,unique=False,nullable=False) 
    resolved_person=db.Column(db.Integer,unique=False,nullable=False) 
    resolved_date=db.Column(db.Date(),nullable=False)
    status=db.Column(db.Integer,unique=False,nullable=True) 
    solution=db.Column(db.String(100),nullable=True)
    complaint_id=db.Column(db.Integer,db.ForeignKey('complaint_reg.id'))
    assigned_date=db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)
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

class Session(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    dev_type=db.Column(db.String(1),nullable=True)
    session_token=db.Column(db.String(200),nullable=False,unique=True)
    exp_time=db.Column(db.DateTime,nullable=False)
    IP=db.Column(db.String(256),nullable=False)
    MAC=db.Column(db.String(256),nullable=False)

class RoleMapping(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(100),nullable=False)
    role_type=db.Column(db.String(100),nullable=False)

class Complaint_reg_constants(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    values=db.Column(db.Integer,unique=True,nullable=False)
    constants=db.Column(db.String(200),nullable=False,unique=True)
    
class issue_category_constants(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    issue_no=db.Column(db.Integer,unique=True,nullable=False)
    issue=db.Column(db.String(200),nullable=False,unique=True)