from flask import request
from db import db
from admin.models import AdminLog

def log_admin_action(admin_id, action):
    log_entry = AdminLog(
        admin_id=admin_id,
        action=action,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log_entry)
    db.session.commit()
