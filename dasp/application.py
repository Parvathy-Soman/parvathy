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
from helpdesk import *


api = Api(application)
api.add_resource(Search_ticket,"/app/ticket_search")
api.add_resource(Status_update,"/app/status")
api.add_resource(Search_user,"/app/search")
api.add_resource(Update_issue,"/app/update")
api.add_resource(Solution_confirmation,"/app/solution")
api.add_resource(Solution_submit,"/app/submit")
#api.add_resource(Status_update,"/app/complaint")
api.add_resource(Complaint_conformation,"/app/complaint")
api.add_resource(student_login,"/app/log")
if __name__ == '__main__':
    db.create_all()
    application.run(debug = True) 