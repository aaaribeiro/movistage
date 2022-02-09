import uuid

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from models import models
from serializers import schemas


class CRUDTicket:
    
    def readTickets(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Tickets).\
            offset(skip).limit(limit).all()
    

    def readTicketById(self, db: Session, id: int):
        return db.query(models.Tickets).get(id)
    

    def createTicket(self, db: Session, payload: schemas.Ticket):
        ticket = models.Tickets(
            ticket_id = payload.ticket_id,
            organization_id = payload.organization_id,
            agent_id = payload.agent_id,
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


    def updateTicket(self, db: Session, payload: schemas.Ticket,
                    dbTicket: models.Tickets):
        dbTicket.organization_id = payload.organization_id
        dbTicket.agent_id = payload.agent_id
        dbTicket.status = payload.status
        dbTicket.category = payload.category
        dbTicket.urgency = payload.urgency
        dbTicket.subject = payload.subject
        dbTicket.created_date = payload.created_date
        dbTicket.sla_first_response = payload.sla_first_response
        dbTicket.sla_solution_date = payload.sla_solution_date
        db.commit()


    def deleteTicket(self, db: Session, id: int):
        dbTicket = self.readTicketById(db, id)
        db.delete(dbTicket)
        db.commit()


class CRUDOrganization:

    def readOrganizations(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Organizations).\
            offset(skip).limit(limit).all()


    def readOrganizationById(self, db: Session, id: str):
        return db.query(models.Organizations).get(id)
       

    def createOrganization(self, db: Session, payload: schemas.Organization):
        dbOrganization = models.Organizations(
            organization_id = payload.organization_id,
            organization_name = payload.organization_name
            )
        db.add(dbOrganization)
        db.commit()


    def updateOrganization(self, db: Session, payload: schemas.Organization,
                            dbOrganization: models.Organizations):
        dbOrganization.organization_name = payload.organization_name
        db.commit()


    def deleteOrganization(self, db: Session, id: int):
        dbOrganization = self.readOrganizationById(db, id)
        db.delete(dbOrganization)
        db.commit()


class CRUDAgent:

    def readAgents(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Agents).\
            offset(skip).limit(limit).all()


    def readAgentById(self, db: Session, id: str):
        return db.query(models.Agents).get(id)


    def createAgent(self, db: Session, payload: schemas.Agent):
        dbAgent = models.Agents(
            agent_id = payload.agent_id,
            agent_name = payload.agent_name,
            agent_team = payload.agent_team,
        )
        db.add(dbAgent)
        db.commit()


    def updateAgent(self, db: Session, payload: schemas.Agent,
                    dbAgent: models.Agents):
        dbAgent.agent_name = payload.agent_name
        dbAgent.agent_team = payload.agent_team
        db.commit()


    def deleteAgent(self, db: Session, id: int):
        dbAgent = self.readAgentById(db, id)
        db.delete(dbAgent)
        db.commit()



class CRUDTimeAppointment:

    def readTimeAppointmentById(self, db:Session, id: int):
        return db.query(models.TimeAppointments).get(id)

    
    # def readTimeAppointmentsByTicketId(self, db:Session, id: int):
    #     return db.query(models.TimeAppointments).\
    #             filter(models.TimeAppointments.ticket_id == id).\
    #             all()


    def createTimeAppointment(self, db: Session,
                                payload: schemas.TimeAppointment):
        dbTimeAppointment = models.TimeAppointments(
            time_appointment_id = payload.time_appointment_id,
            ticket_id = payload.ticket_id,
            agent_id = payload.agent_id,
            time_appointment = payload.time_appointment,
            created_date = payload.created_date,
        )
        db.add(dbTimeAppointment)   
        db.commit()


    # def delete_time_appointments_by_ticket_id(self, db: Session, id: int):
    #     dbtimes = self.read_time_appointments_by_ticket_id(db, id)
    #     for dbtime in dbtimes:
    #         db.delete(dbtime)
    #     db.commit()


# class Crud(CRUDAgent, CRUDOrganization, CRUDTimeAppointment, CRUDTicket):

#     def createUpdateTicket(self, db: Session, payload: schemas.TicketNestedCompany):
#         # check agent
#         dbAgent = self.readAgentById(db, payload.agent.agent_id)
#         if not dbAgent:
#             self.createAgent(db, payload.agent)
#         else:
#             self.updateAgent(db, payload.agent, dbAgent)

#         # check organization
#         dbOrganization = self.readOrganizationById(db,
#                                         payload.organization.organization_id)
#         if not dbOrganization:
#             self.createOrganization(db, payload.organization)
#         else:
#             self.updateOrganization(db, payload.organization, dbOrganization)

#         # check ticket
#         dbTicket = self.readTicketById(db, payload.ticket_id)
#         if not dbTicket:
#             self.createTicket(db, payload)
#         else:
#             self.updateTicket(db, payload, dbTicket) 

#         # check each time appointment
#         for appointment in payload.appointments:
#             dbTimeAppointment = self.readTimeAppointmentById(db,
#                                                 appointment.time_appointment_id)
#             if not dbTimeAppointment:
#                 self.createTimeAppointment(db, appointment)
#             else:
#                 self.updateTimeAppointment(db, appointment, dbTimeAppointment)




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
    # db_hook_updated = get_hook_by_id(
    #     db,
    #     id=id
    # )
    # return db_hook_updated