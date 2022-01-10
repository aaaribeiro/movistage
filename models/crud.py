# import logging # library for logging
# import logging.config # logging config file

# logging.config.fileConfig("logging.config")
# logger = logging.getLogger("sqlalchemy")

import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from models import models
from serializers import schemas


### TICKETS ###

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tickets).offset(
        skip).limit(limit).all()


def get_ticket_by_id(db: Session, id: int):
    return db.query(models.Tickets).filter(
        models.Tickets.ticket_id==id).first()


def create_ticket(db: Session, ticket: schemas.Ticket):
    db_ticket = models.Tickets(
        ticket_id = ticket.ticket_id,
        client_id = ticket.client_id,
        status = ticket.status,
        owner_team = ticket.owner_team,
        agent = ticket.agent,
        category = ticket.category,
        urgency = ticket.urgency,
        subject = ticket.subject,
        created_date = ticket.created_date,
        sla_solution_date = ticket.sla_solution_date,
        sla_first_response = ticket.sla_first_response
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def partial_update_ticket(db: Session, id: str, 
                        ticket: schemas.Ticket):
    db.query(models.Tickets).filter(
        models.Tickets.ticket_id==id).update(
        ticket.dict(exclude_unset=True))        
    db.commit()
    # db.flush()
    db_ticket_updated = get_ticket_by_id(
        db,
        id=id
    )
    return db_ticket_updated


def delete_ticket(db: Session, id: int):
    db_ticket = get_ticket_by_id(db, id)
    db.delete(db_ticket)
    db.commit()
    # db.flush()
    return True 


### ORGANIZATIONS ###

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organizations).offset(
        skip).limit(limit).all()


def get_customer_by_id(db: Session, id: str):
    return db.query(models.Organizations).filter(
        models.Organizations.client_id==id).first()


def create_organization(db: Session, organization: schemas.Organization):
    customer = models.Organizations(
        client_id = organization.client_id,
        organization_name = organization.organization_name
        )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def partial_update_organization(db: Session, id: str, 
                                organization: schemas.Organization):
    db.query(models.Organizations).filter(
        models.Organizations.client_id==id).update(
        organization.dict(exclude_unset=True))        
    db.commit()
    # db.flush()
    db_organization_updated = get_customer_by_id(
        db,
        id=id
    )
    return db_organization_updated


def delete_organization(db: Session, id: str):
    db_organization = get_customer_by_id(db, id)
    db.delete(db_organization)
    db.commit()
    return True 


### TIME APPOINTMENTS ###

def get_time_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TimeAppointments).offset(
        skip).limit(limit).all()


def get_time_appointment_by_ticket_id(db: Session, ticket_id: int):
    return db.query(models.TimeAppointments).filter(
        models.TimeAppointments.ticket_id==ticket_id).first()
    

def get_time_appointment_max_id(db: Session):
    return db.query(func.max(
        models.TimeAppointments.ticket_time_appointment_pk)).first()


def create_time_appointment(db: Session,
                            time_appointment: schemas.TimeAppointment):
    db_time_appointment = models.TimeAppointments(
        # ticket_time_appointment_pk = get_time_appointment_max_id(db)[0] + 1,
        ticket_id = time_appointment.ticket_id,
        time_appointment = time_appointment.time_appointment,
        agent = time_appointment.agent
    )
    db.add(db_time_appointment)
    db.commit()
    db.refresh(db_time_appointment)
    return db_time_appointment


### WEBHOOK ###

def get_hook_logs(db: Session, read: bool = None,
                    skip: int = 0, limit: int = 100):
    if read is not None:
        return db.query(models.WebhookLogs).\
            filter(models.WebhookLogs.was_read==read).\
            order_by(models.WebhookLogs.hook_id).\
            offset(skip).limit(limit).all()
            
    else:
        return db.query(models.WebhookLogs).\
            offset(skip).limit(limit).all()


def get_hooks_by_ticket_id(db: Session, ticket_id: int, skip: int = 0,
    limit: int = 100):
    return db.query(models.WebhookLogs).\
        filter(models.WebhookLogs.ticket_id==ticket_id).\
        offset(skip).limit(limit).all()


def get_hook_log_by_ticket_id(db: Session, ticket_id: int):
    return db.query(models.WebhookLogs).filter(
        models.WebhookLogs.ticket_id==ticket_id).first()


def create_hook(db: Session, webhook: schemas.WebhookLog):
    db_webhook = models.WebhookLogs(
        ticket_id = webhook.ticket_id,
        change = webhook.change,
        trigger_date = webhook.trigger_date,
    )
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return True


## USER

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(
        models.Users.email==email).first()


def register_user(db: Session, user: schemas.User):
    db_user = models.Users(
        # id = webhook.ticket_id,
        name = user.name,
        email = user.email,
        isadmin = user.isadmin,
        password = user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_access_token(db: Session, user: schemas.CreatedUser):
    return db.query(models.AccessToken).filter(
        models.AccessToken.user_id==user.user_id).first()


def create_access_token(db: Session, user: schemas.CreatedUser):
    db_token = models.AccessToken(
        user_id = user.user_id,
        access_token = uuid.uuid5(uuid.uuid4(), user.email)
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def authenticate_user(db: Session, user: str, password: str):
    user = get_user_by_email(db, email=user)
    if not user:
        return
    if password != user.password:
        return
    return user


def get_user_by_token(db: Session, token: str):
    return db.query(models.AccessToken.access_token,
                    models.Users.email,
                    models.Users.isadmin).\
            join(models.Users).filter(
        models.AccessToken.access_token==token).first()


# def delete_token(db: Session, token_model: models.AccessToken):
#     db.delete(token_model)
#     db.commit()
#     return True


def get_token_by_user_id(db: Session, id: int):
    return db.query(models.AccessToken).filter(
        models.AccessToken.user_id == id).first()


def get_hook_by_id(db: Session, id: int):
    return db.query(models.WebhookLogs).filter(
        models.WebhookLogs.hook_id==id).first()


def partial_update_hook(db: Session, id: str, 
                        hook: schemas.WebhookLog):
    db.query(models.WebhookLogs).filter(
        models.WebhookLogs.hook_id==id).update(
        hook.dict(exclude_unset=True))        
    db.commit()
    db_hook_updated = get_hook_by_id(
        db,
        id=id
    )
    return db_hook_updated