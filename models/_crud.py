# from sqlite3 import IntegrityError
# import psycopg2
import uuid

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError

from models import models
from routers import organizations
from serializers import schemas


class CRUDTicket:

    def read_tickets(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Tickets).\
            offset(skip).limit(limit).all()
    

    def read_ticket_by_id(self, db: Session, id: int):
        return db.query(models.Tickets).get(id)
    

    def create_ticket(self, db: Session, payload: schemas.TicketNestedCompany):
        _agent = payload.agent
        self.__check_agent(db, _agent)
        
        _organization = payload.organization
        self.__check_organization(db, _organization)

        ticket = models.Tickets(
            ticket_id = payload.ticket_id,
            organization_id = payload.organization.organization_id,
            agent_id = payload.agent.agent_id,
            status = payload.status,
            category = payload.category,
            urgency = payload.urgency,
            subject = payload.subject,
            created_date = payload.created_date,
            sla_solution_date = payload.sla_solution_date,
            sla_first_response = payload.sla_first_response,
        )
        db.add(ticket)
        db.commit()


    def update_ticket(self, db: Session, payload: schemas.TicketNestedCompany,
                        dbticket: models.Tickets):
        _agent = payload.agent
        self.__check_agent(db, _agent)
        
        _organization = payload.organization
        self.__check_organization(db, _organization)

        dbticket.organization_id = payload.organization.organization_id
        dbticket.agent_id = payload.agent.agent_id
        dbticket.status = payload.status
        dbticket.category = payload.category
        dbticket.urgency = payload.urgency
        dbticket.subject = payload.subject
        dbticket.created_date = payload.created_date
        dbticket.sla_first_response = payload.sla_first_response
        dbticket.sla_solution_date = payload.sla_solution_date
        db.commit()


    def delete_ticket(self, db: Session, id: int):
        dbticket = self.read_ticket_by_id(db, id)
        db.delete(dbticket)
        db.commit()


    def __check_agent(self, db: Session, payload: schemas.Agent):
        _crud = CRUDAgent()
        _agent = _crud.read_agent_by_id(payload.organization_id)
        if not _agent:
            _crud.create_agent(db, payload)


    def __check_organization(self, db: Session,
                            payload: schemas.Organization):
        _crud = CRUDOrganization()
        _organization = _crud.read_organization_by_id(payload.organization_id)
        if not _organization:
            _crud.create_organization(db, payload)




class CRUDOrganization:
    
    def read_organization_by_id(self, db: Session, id: str):
        return db.query(models.Organizations).get(id)
       

    def create_organization(self, db: Session, payload: schemas.Organization):
        organization = models.Organizations(
            organization_id = payload.organization_id,
            organization_name = payload.organization_name
            )
        db.add(organization)
        db.commit()



class CRUDAgent:

    def read_agent_by_id(self, db: Session, id: str):
        return db.query(models.Agents).get(id)


    def create_agent(self, db: Session, agent: schemas.Agent):
        dbagent = models.Agents(
            agent_id = agent.agent_id,
            agent_name = agent.agent_name,
            agent_team = agent.agent_team,
        )
        db.add(dbagent)
        db.commit()


# agents
# def read_agent_by_id(db: Session, id: str):
#     agent = db.query(models.Agents).get(id)
#     return agent


# def create_agent(db: Session, agent: schemas.Agent):
#     db_agent = models.Agents(
#         agent_id = agent.agent_id,
#         agent_name = agent.agent_name,
#         agent_team = agent.agent_team,
#     )
#     db.add(db_agent)
#     db.commit()


# def partial_update_ticket(db: Session, id: str, 
#                         ticket: schemas.Ticket):
#     db.query(models.Tickets).filter(
#         models.Tickets.ticket_id==id).update(
#         ticket.dict(exclude_unset=True))        
#     db.commit()



# def delete_ticket(db: Session, id: int):
#     db_ticket = get_ticket_by_id(db, id)
#     db.delete(db_ticket)
#     db.commit()


### ORGANIZATIONS ###
# def read_organizations(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Organizations).offset(
#         skip).limit(limit).all()


# def read_organization_by_id(db: Session, id: str):
#     organization = db.query(models.Organizations).get(id)
#     return organization 


# def create_organization(db: Session, organization: schemas.Organization):
#     customer = models.Organizations(
#         organization_id = organization.organization_id,
#         organization_name = organization.organization_name
#         )
#     db.add(customer)
#     db.commit()


# def partial_update_organization(db: Session, id: str, 
#                                 organization: schemas.Organization):
#     db.query(models.Organizations).filter(
#         models.Organizations.client_id==id).update(
#         organization.dict(exclude_unset=True))        
#     try:
#         db.commit()
#     except IntegrityError as err:
#         db.rollback()
#         print(err)
    # db.flush()
    # db_organization_updated = get_customer_by_id(
    #     db,
    #     id=id
    # )
    # return db_organization_updated


# def delete_organization(db: Session, id: str):
#     db_organization = get_customer_by_id(db, id)
#     db.delete(db_organization)
#     db.commit()
#     return True 


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
    # db.refresh(db_time_appointment)
    # return db_time_appointment


### WEBHOOK ###

# def get_hook_logs(db: Session, read: bool = None,
#                     skip: int = 0, limit: int = 100):
#     if read is not None:
#         return db.query(models.WebhookLogs).\
#             filter(models.WebhookLogs.was_read==read).\
#             order_by(models.WebhookLogs.hook_id).\
#             offset(skip).limit(limit).all()
            
#     else:
#         return db.query(models.WebhookLogs).\
#             offset(skip).limit(limit).all()


# def get_hooks_by_ticket_id(db: Session, ticket_id: int, skip: int = 0,
#     limit: int = 100):
#     return db.query(models.WebhookLogs).\
#         filter(models.WebhookLogs.ticket_id==ticket_id).\
#         offset(skip).limit(limit).all()


# def get_hook_log_by_ticket_id(db: Session, ticket_id: int):
#     return db.query(models.WebhookLogs).filter(
#         models.WebhookLogs.ticket_id==ticket_id).first()


# def create_hook(db: Session, webhook: schemas.WebhookLog):
#     db_webhook = models.WebhookLogs(
#         ticket_id = webhook.ticket_id,
#         change = webhook.change,
#         trigger_date = webhook.trigger_date,
#     )
#     db.add(db_webhook)
#     db.commit()
    # db.refresh(db_webhook)
    # return True


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


# def get_hook_by_id(db: Session, id: int):
#     return db.query(models.WebhookLogs).filter(
#         models.WebhookLogs.hook_id==id).first()


# def partial_update_hook(db: Session, id: str, 
#                         hook: schemas.WebhookLog):
#     db.query(models.WebhookLogs).filter(
#         models.WebhookLogs.hook_id==id).update(
#         hook.dict(exclude_unset=True))        
#     db.commit()
    # db_hook_updated = get_hook_by_id(
    #     db,
    #     id=id
    # )
    # return db_hook_updated