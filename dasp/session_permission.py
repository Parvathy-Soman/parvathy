from model import *
def checkSessionValidity(sessionid,userid):
    chk_user=Session.query.filter(Session.session_token==sessionid,Session.uid==userid,Session.exp_time>datetime.now()).first()          
    if chk_user:         
        return True     
    else:         
        return False 
