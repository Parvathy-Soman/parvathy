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
from flask_cors import CORS

api = Api(application)
CORS(application)
api.add_resource(Search_ticket,"/app/ticket_search")
api.add_resource(Status_update,"/app/status")
api.add_resource(Assign_users,"/app/users_list")
api.add_resource(Assign_submit,"/app/submit_assignee")

# api.add_resource(Search_user,"/app/search")
# api.add_resource(Update_issue,"/app/update")
# api.add_resource(Solution_confirmation,"/app/solution")
# api.add_resource(Solution_submit,"/app/submit")
#api.add_resource(Status_update,"/app/complaint")
# api.add_resource(Complaint_conformation,"/app/complaint")
# api.add_resource(student_login,"/app/log")
# api.add_resource(Ticket_assign,"/app/assign")
# api.add_resource(StudMyProgramme, '/api/stud_myprogramme_list')

api.add_resource(Search_user,"/app/search")
# api.add_resource(Complaint_registration,"/app/com_reg")
api.add_resource(Complaint_registration,"/app/complaint_con")
api.add_resource(Complaint_Reopen,"/app/reopen")
api.add_resource(Complaint_previous,"/app/previous")
api.add_resource(All_complaints,"/app/all_complaints")
# api.add_resource(Escalation_module,"/app/es_start")
# api.add_resource(Escalation_module_to_unstaff_submit,"/app/es_to_unstaff_submit")
# api.add_resource(Escalation_module_to_unstaff_confirmation,"/app/es_to_unstaff_confirm")
# api.add_resource(Tickets_total_view,"/app/tickets_view")
# api.add_resource(pending_ticket_view,"/app/pending_ticket_view")
# api.add_resource(Tickets_day_view,"/app/pending_tickets_singleday")
# api.add_resource(finding_assigned_persons_id,"/app/assignedperson_id")
api.add_resource(AllComp,"/app/my_test")
if __name__ == '__main__':
    db.create_all()
    application.run(debug = True) 