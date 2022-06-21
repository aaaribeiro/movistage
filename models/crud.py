import uuid

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from models import models
from serializers import schemas


class CRUDTicket:
    
    def readTickets(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Tickets).\
            order_by(models.Tickets.ticket_id).all()

    

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

    def readTimeAppointments(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.TimeAppointments).\
            offset(skip).limit(limit).all()


    def readTimeAppointmentById(self, db:Session, id: int):
        return db.query(models.TimeAppointments).get(id)

    
    def readTimeAppointmentsByTicketId(self, db:Session, id: int):
        return db.query(models.TimeAppointments).\
                filter(models.TimeAppointments.ticket_id == id).\
                all()


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


    def updateTimeAppointment(self, db: Session, payload: schemas.TimeAppointment,
                    dbAppointment: models.TimeAppointments):
        dbAppointment.ticket_id = payload.ticket_id
        dbAppointment.agent_id = payload.agent_id
        dbAppointment.created_date = payload.created_date
        dbAppointment.time_appointment = payload.time_appointment
        db.commit()

    def updateTimeAppointment(self, db: Session, payload: schemas.TimeAppointment, 
                                dbAppointment: models.TimeAppointments):
        dbAppointment.agent_id = payload.agent_id
        dbAppointment.ticket_id = payload.ticket_id
        dbAppointment.time_appointment = payload.time_appointment
        dbAppointment.created_date = payload.created_date
        db.commit()
                

    def deleteTimeAppointmentsByTicketId(self, db: Session, id: int):
        dbAppointments = self.readTimeAppointmentsByTicketId(db, id)
        for dbAppointment in dbAppointments:
            db.delete(dbAppointment)
        db.commit()
    

    def deleteTimeAppointment(self, db: Session, id: int):
        dbAppointment = self.readTimeAppointmentById(db, id)
        db.delete(dbAppointment)
        db.commit()



class CRUDUser:

    def readUserByEmail(self, db: Session, email: str):
        return db.query(models.Users).\
            filter(models.Users.email==email).\
            first()


    def createUser(self, db: Session, user: schemas.User):
        dbUser = models.Users(
            name = user.name,
            email = user.email,
            isadmin = user.isadmin,
            password = user.password,
        )
        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)
        return dbUser


    def readAccessToken(self, db: Session, user: schemas.CreatedUser):
        return db.query(models.AccessToken).filter(
            models.AccessToken.user_id==user.user_id).first()


    def createAccessToken(self, db: Session, user: schemas.CreatedUser):
        dbToken = models.AccessToken(
            user_id = user.user_id,
            access_token = uuid.uuid5(uuid.uuid4(), user.email)
        )
        db.add(dbToken)
        db.commit()
        db.refresh(dbToken)
        return dbToken


    def authenticate_user(self, db: Session, user: str, password: str):
        user = self.readUserByEmail(db, email=user)
        if not user:
            return
        if password != user.password:
            return
        return user


    def readUserByToken(self, db: Session, token: str):
        return db.query(models.AccessToken.access_token, models.Users.email,
                        models.Users.isadmin).\
                join(models.Users).\
                filter(models.AccessToken.access_token==token).\
                first()


    def readTokenByUserId(self, db: Session, id: int):
        return db.query(models.AccessToken).filter(
            models.AccessToken.user_id == id).first()
