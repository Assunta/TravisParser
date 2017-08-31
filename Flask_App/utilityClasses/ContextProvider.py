import logging
from flask import request, session
class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        if(session.get('username')):
            log_record.user_id = session['username']
        else:
            log_record.user_id = "no user"
        return True